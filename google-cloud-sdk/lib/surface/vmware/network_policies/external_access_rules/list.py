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
"""'vmware external-access-rules list' command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.vmware.externalaccessrules import ExternalAccessRulesClient
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.vmware.network_policies import flags

DETAILED_HELP = {
    'DESCRIPTION':
        """
          List VMware Engine external access firewall rules.
        """,
    'EXAMPLES':
        """
          To list external access firewall rules in your project in the region ``us-west2'' associated with network policy ``my-network-policy'', sorted from oldest to newest, run:

            $ {command} --location=us-west2 --project=my-project --network-policy=my-network-policy --sort-by=~create_time

          Or:

            $ {command}  --sort-by=~create_time --network-policy=my-network-policy

          In the second example, the project and the location are taken from gcloud properties core/project and compute/region respectively.
    """,
}


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.GA)
class List(base.ListCommand):
  """List VMware Engine external access rules."""
  detailed_help = DETAILED_HELP

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    flags.AddNetworkPolicyToParser(parser)
    parser.display_info.AddFormat(
        'table(name.segment(-1):label=NAME,'
        'priority,ipProtocol,sourceIpRanges,'
        'sourcePorts,destinationIpRanges,destinationPorts,'
        'action)')

  def Run(self, args):
    network_policy = args.CONCEPTS.network_policy.Parse()
    client = ExternalAccessRulesClient()
    return client.List(network_policy)
