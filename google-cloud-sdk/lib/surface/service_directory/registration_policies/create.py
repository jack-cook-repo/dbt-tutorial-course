# -*- coding: utf-8 -*- #
# Copyright 2022 Google Inc. All Rights Reserved.
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
"""`gcloud service-directory registration-policies create` command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.service_directory import registration_policies
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.service_directory import flags
from googlecloudsdk.command_lib.service_directory import resource_args
from googlecloudsdk.command_lib.service_directory import util
from googlecloudsdk.core import log

_RESOURCE_TYPE = 'registration_policy'


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA)
@base.Hidden
class CreateBeta(base.CreateCommand):
  """Creates a registration policy."""

  detailed_help = {
      'EXAMPLES':
          """\
          To create a Service Directory registration policy, run:

            $ {command} --location=my-location --policy-from-file=~/my-policy.yaml
          """,
  }

  @staticmethod
  def Args(parser):
    resource_args.AddLocationResourceArg(parser, 'to create', positional=False)
    flags.AddPolicyFlag(parser)

  def Run(self, args):
    client = registration_policies.RegistrationPoliciesClient()
    location_ref = args.CONCEPTS.location.Parse()

    policy = args.policy_from_file
    util.ValidatePolicyFile(policy)

    result = client.Create(location_ref, policy)
    log.CreatedResource(policy['metadata']['name'], _RESOURCE_TYPE)

    return result
