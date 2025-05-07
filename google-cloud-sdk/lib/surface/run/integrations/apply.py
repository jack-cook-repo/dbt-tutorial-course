# -*- coding: utf-8 -*- #
# Copyright 2021 Google LLC. All Rights Reserved.
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
"""Command for creating or replacing an application from YAML specification."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import exceptions
from googlecloudsdk.command_lib.run import flags as run_flags
from googlecloudsdk.command_lib.run.integrations import flags
from googlecloudsdk.command_lib.run.integrations import run_apps_operations
from googlecloudsdk.command_lib.run.integrations import stages
from googlecloudsdk.core import yaml
from googlecloudsdk.core.console import progress_tracker


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Apply(base.Command):
  """Create or replace an application from a YAML specification."""

  detailed_help = {
      'DESCRIPTION':
          """\
          {description}
          """,
      'EXAMPLES':
          """\
          To create an application from specification

              $ {command} stack.yaml

         """,
  }

  @classmethod
  def Args(cls, parser):
    flags.AddFileArg(parser)

  def _ValidateAppConfigFile(self, file_content):
    if 'name' not in file_content:
      raise exceptions.FieldMismatchError("'name' is missing.")

  def Run(self, args):
    """Create or Update application from YAML."""

    self._ValidateAppConfigFile(args.FILE)
    app_dict = dict(args.FILE)
    name = app_dict.pop('name')
    appconfig = {'config': yaml.dump(args.FILE).encode('utf-8')}
    release_track = self.ReleaseTrack()

    conn_context = connection_context.GetConnectionContext(
        args, run_flags.Product.RUN_APPS, release_track)
    with run_apps_operations.Connect(conn_context, release_track) as client:

      with progress_tracker.StagedProgressTracker(
          'Applying Configuration...',
          stages.ApplyStages(),
          failure_message='Failed to apply application configuration.'
      ) as tracker:
        return client.ApplyAppConfig(tracker, name, appconfig)
