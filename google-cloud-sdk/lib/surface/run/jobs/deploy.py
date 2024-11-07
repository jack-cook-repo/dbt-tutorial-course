# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Deploy a container to Cloud Run that will run to completion."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import enum
import os.path

from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions as c_exceptions
from googlecloudsdk.command_lib.artifacts import docker_util
from googlecloudsdk.command_lib.run import artifact_registry
from googlecloudsdk.command_lib.run import config_changes
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import messages_util
from googlecloudsdk.command_lib.run import pretty_print
from googlecloudsdk.command_lib.run import resource_args
from googlecloudsdk.command_lib.run import serverless_operations
from googlecloudsdk.command_lib.run import stages
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core.console import console_io
from googlecloudsdk.core.console import progress_tracker


class BuildType(enum.Enum):
  DOCKERFILE = 'Dockerfile'
  BUILDPACKS = 'Buildpacks'


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA)
class Deploy(base.Command):
  """Create or update a Cloud Run job."""

  detailed_help = {
      'DESCRIPTION': """\
          Creates or updates a Cloud Run job.
          """,
      'EXAMPLES': """\
          To deploy a new job `my-data-transformation` to Cloud Run:

              $ {command} my-data-transformation --image=us-docker.pkg.dev/project/image

          You may also omit the job name. Then a prompt will be displayed
          with a suggested default value:

              $ {command} --image=us-docker.pkg.dev/project/image
          """,
  }

  @staticmethod
  def CommonArgs(parser):
    job_presentation = presentation_specs.ResourcePresentationSpec(
        'JOB',
        resource_args.GetJobResourceSpec(prompt=True),
        'Job to deploy.',
        required=True,
        prefixes=False,
    )
    flags.AddLabelsFlag(parser)
    flags.AddParallelismFlag(parser)
    flags.AddTasksFlag(parser)
    flags.AddMaxRetriesFlag(parser)
    flags.AddTaskTimeoutFlags(parser)
    flags.AddServiceAccountFlag(parser, managed_only=True)
    flags.AddMutexEnvVarsFlags(parser)
    flags.AddSetCloudSQLFlag(parser)
    flags.AddVpcConnectorArg(parser)
    flags.AddEgressSettingsFlag(parser)
    flags.AddSetSecretsFlag(parser)
    flags.AddMemoryFlag(parser)
    flags.AddCpuFlag(parser, managed_only=True)
    flags.AddCommandFlag(parser)
    flags.AddArgsFlag(parser)
    flags.AddClientNameAndVersionFlags(parser)
    flags.AddBinAuthzPolicyFlags(parser, with_clear=False)
    flags.AddBinAuthzBreakglassFlag(parser)
    flags.AddCmekKeyFlag(parser, with_clear=False)
    flags.AddSandboxArg(parser, hidden=True)
    flags.AddGeneralAnnotationFlags(parser)
    flags.AddVpcNetworkFlags(parser, resource_kind='Job')
    flags.AddVpcSubnetFlags(parser, resource_kind='Job')
    flags.AddVpcNetworkTagsFlags(parser, resource_kind='Job')
    flags.AddSourceAndImageFlags(
        parser, image='us-docker.pkg.dev/cloudrun/container/job:latest'
    )

    polling_group = parser.add_mutually_exclusive_group()
    flags.AddAsyncFlag(polling_group)
    flags.AddWaitForCompletionFlag(polling_group, implies_execute_now=True)

    flags.AddExecuteNowFlag(parser)

    concept_parsers.ConceptParser([job_presentation]).AddToParser(parser)
    # No output by default, can be overridden by --format
    parser.display_info.AddFormat('none')

  @staticmethod
  def Args(parser):
    Deploy.CommonArgs(parser)

  def Run(self, args):
    """Deploy a Job to Cloud Run."""
    include_build = flags.FlagIsExplicitlySet(args, 'source')
    if not include_build and not args.IsSpecified('image'):
      if console_io.CanPrompt():
        args.source = flags.PromptForDefaultSource()
        include_build = True
      else:
        raise c_exceptions.RequiredArgumentException(
            '--image',
            (
                'Requires a container image to deploy (e.g.'
                ' `us-docker.pkg.dev/cloudrun/container/job:latest`) if no'
                ' build source is provided.'
            ),
        )

    job_ref = args.CONCEPTS.job.Parse()
    flags.ValidateResource(job_ref)

    conn_context = connection_context.GetConnectionContext(
        args, flags.Product.RUN, self.ReleaseTrack()
    )

    build_type = None
    image = None
    pack = None
    source = None
    operation_message = 'Deploying container to'
    repo_to_create = None
    # Build an image from source if source specified
    if include_build:
      source = args.source

      ar_repo = docker_util.DockerRepo(
          project_id=properties.VALUES.core.project.Get(required=True),
          location_id=artifact_registry.RepoRegion(args),
          repo_id='cloud-run-source-deploy',
      )
      if artifact_registry.ShouldCreateRepository(ar_repo):
        repo_to_create = ar_repo
      # The image is built with latest tag. After build, the image digest
      # from the build result will be added to the image of the job spec.
      args.image = '{repo}/{job}'.format(
          repo=ar_repo.GetDockerString(), job=job_ref.jobsId
      )
      # Use GCP Buildpacks if Dockerfile doesn't exist
      docker_file = source + '/Dockerfile'
      if os.path.exists(docker_file):
        build_type = BuildType.DOCKERFILE
      else:
        pack = [{'image': args.image}]
        if self.ReleaseTrack() is base.ReleaseTrack.ALPHA:
          command_arg = getattr(args, 'command', None)
          if command_arg is not None:
            command = ' '.join(command_arg)
            pack[0].update(
                {'env': 'GOOGLE_ENTRYPOINT="{command}"'.format(command=command)}
            )
        build_type = BuildType.BUILDPACKS
      image = None if pack else args.image
      operation_message = (
          'Building using {build_type} and deploying container to'
      ).format(build_type=build_type.value)
      pretty_print.Info(
          messages_util.GetBuildEquivalentForSourceRunMessage(
              job_ref.jobsId, pack, source, is_job=True
          )
      )

    changes = flags.GetJobConfigurationChanges(args)
    changes.append(
        config_changes.SetLaunchStageAnnotationChange(self.ReleaseTrack())
    )

    execute_now = args.execute_now or args.wait
    execution = None

    with serverless_operations.Connect(conn_context) as operations:
      job_obj = operations.GetJob(job_ref)
      pretty_print.Info(
          messages_util.GetStartDeployMessage(
              conn_context, job_ref, operation_message, 'job'
          )
      )
      header_msg = None
      operation = 'Creating' if job_obj is None else 'Updating'
      if include_build and execute_now:
        header_msg = 'Building, {} and running job...'.format(operation.lower())
      elif include_build:
        header_msg = 'Building and {} job...'.format(operation.lower())
      elif execute_now:
        header_msg = '{} and running job...'.format(operation)
      else:
        header_msg = '{} job...'.format(operation)
      with progress_tracker.StagedProgressTracker(
          header_msg,
          stages.JobStages(
              execute_now=execute_now,
              include_completion=args.wait,
              include_build=include_build,
              include_create_repo=repo_to_create is not None,
          ),
          failure_message='Job failed to deploy',
          suppress_output=args.async_,
      ) as tracker:
        job = operations.DeployJob(
            job_ref,
            changes,
            tracker,
            asyn=(args.async_ and not execute_now),
            build_image=image,
            build_pack=pack,
            build_source=source,
            repo_to_create=repo_to_create,
            prefetch=job_obj,
        )
        if execute_now:
          execution = operations.RunJob(
              job_ref, args, tracker, self.ReleaseTrack()
          )

      if args.async_ and not execute_now:
        pretty_print.Success(
            'Job [{{bold}}{job}{{reset}}] is being deployed '
            'asynchronously.'.format(job=job.name)
        )
      else:
        job = operations.GetJob(job_ref)
        operation = 'been deployed'
        if args.wait:
          operation += ' and completed execution [{}]'.format(execution.name)
        elif execute_now:
          operation += ' and started running execution [{}]'.format(
              execution.name
          )

        pretty_print.Success(
            'Job [{{bold}}{job}{{reset}}] has successfully {operation}.'.format(
                job=job.name, operation=operation
            )
        )

      msg = ''
      if execute_now:
        msg += messages_util.GetExecutionCreatedMessage(
            self.ReleaseTrack(), execution
        )
        msg += '\n'
      msg += messages_util.GetRunJobMessage(
          self.ReleaseTrack(), job.name, repeat=execute_now
      )
      log.status.Print(msg)
      return job
