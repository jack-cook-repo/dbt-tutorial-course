# -*- coding: utf-8 -*- #
# Copyright 2023 Google LLC. All Rights Reserved.
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
"""The command to create a Workload Registration."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.workload_certificate import client
from googlecloudsdk.calliope import base as calliope_base


class Create(calliope_base.CreateCommand):

  """Create a Workload Registration resource.

  Create a Workload Registration resource in a fleet.

  ## Examples

  To Create a Workload Registration, run:

    $ {command} wrname --fleet-membership mema --location us-central1 --type k8s
  """

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'workload_registration_id',
        help=(
            'Workload registration ID. This can be any unique string that'
            " matches the regex ^[a-zA-Z0-9-._~%!$&'()*+,;=@]+$ and has"
            ' 1-63 characters in length.'
        ),
    )
    parser.add_argument(
        '--location',
        required=True,
        help=(
            'Location of workload registration. Currently this should be the'
            ' same as the location of fleet membership, but this behavior is'
            ' subject to change.'
        ),
    )
    parser.add_argument(
        '--fleet-membership',
        required=True,
        help=(
            'Fleet membership. If `gcloud` was used to register the membership'
            ' command, this is the membership name passed to the `gcloud'
            ' container fleet memberships register`.'
        ),
    )
    parser.add_argument(
        '--type',
        required=True,
        choices=['k8s', 'kubernetes'],
        help='Workload type. Only GKE workloads are supported.',
    )

  def Run(self, args):
    return client.WIPClient(self.ReleaseTrack()).CreateRegistration(
        args.location, args.fleet_membership, args.workload_registration_id
    )
