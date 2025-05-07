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
"""'vmware private-clouds create' command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.vmware.privateclouds import PrivateCloudsClient
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.vmware import flags
from googlecloudsdk.core import log

DETAILED_HELP = {
    'DESCRIPTION':
        """
          Create a VMware Engine private cloud. Private cloud creation is considered finished when the private cloud is in READY state. Check the progress of a private cloud using `{parent_command} list`.
        """,
    'EXAMPLES':
        """
          To create a private cloud in the ``us-west2-a'' zone using ``standard-72'' nodes that connects to the ``my-network'' VMware Engine network, run:


          $ {command} my-private-cloud --location=us-west2-a --project=my-project --cluster=my-management-cluster --node-type-config=type=standard-72,count=3 --management-range=192.168.0.0/24 --vmware-engine-network=my-network

          Or:

          $ {command} my-private-cloud --cluster=my-management-cluster --node-type-config=type=standard-72,count=3 --management-range=192.168.0.0/24 --vmware-engine-network=my-network

          In the second example, the project and location are taken from gcloud properties core/project and compute/zone.
    """,
}


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Create(base.CreateCommand):
  """Create a VMware Engine private cloud."""

  detailed_help = DETAILED_HELP

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    flags.AddPrivatecloudArgToParser(parser, positional=True)
    flags.AddClusterArgToParser(parser, positional=False)
    base.ASYNC_FLAG.AddToParser(parser)
    base.ASYNC_FLAG.SetDefault(parser, True)
    parser.add_argument(
        '--description',
        help="""\
        Text describing the private cloud.
        """)
    parser.add_argument(
        '--management-range',
        required=True,
        help="""\
         IP address range in the private cloud to use for management appliances, in CIDR format. Use an IP address range that meets the [VMware Engine networking requirements](https://cloud.google.com/vmware-engine/docs/quickstart-networking-requirements).
        """)
    parser.add_argument(
        '--vmware-engine-network',
        required=True,
        help="""\
        Resource ID of the VMware Engine network attached to the private cloud.
        """)
    parser.add_argument(
        '--node-type-config',
        required=True,
        type=arg_parsers.ArgDict(
            spec={
                'type': str,
                'count': int,
                'custom-core-count': int
            },
            required_keys=('type', 'count')),
        action='append',
        help="""\
        Information about the type and number of nodes associated with the cluster.

        type (required): canonical identifier of the node type.

        count (required): number of nodes of this type in the cluster.

        custom-core-count (optional): customized number of cores available to each node of the type.
        To get a list of valid values for your node type,
        run the gcloud vmware node-types describe command and reference the
        availableCustomCoreCounts field in the output.
        """)
    parser.add_argument(
        '--type',
        required=False,
        hidden=True,
        default='STANDARD',
        choices={
            'STANDARD': """Standard private is a zonal resource, with 3 or more nodes nodes. Default type.""",
            'TIME_LIMITED': """Time limited private cloud is a zonal resource, can have only 1 node and
            has limited life span. Will be deleted after defined period of time,
            can be converted into standard private cloud by expanding it up to 3
            or more nodes"""},
        help='Type of the private cloud')

  def Run(self, args):
    privatecloud = args.CONCEPTS.private_cloud.Parse()
    client = PrivateCloudsClient()
    is_async = args.async_
    operation = client.Create(
        privatecloud,
        cluster_id=args.cluster,
        nodes_configs=args.node_type_config,
        network_cidr=args.management_range,
        vmware_engine_network_id=args.vmware_engine_network,
        description=args.description,
        private_cloud_type=args.type,
    )
    if is_async:
      log.CreatedResource(operation.name, kind='private cloud', is_async=True)
      return operation

    resource = client.WaitForOperation(
        operation_ref=client.GetOperationRef(operation),
        message='waiting for private cloud [{}] to be created'.format(
            privatecloud.RelativeName()
        ),
    )
    log.CreatedResource(resource, kind='private cloud')

    return resource
