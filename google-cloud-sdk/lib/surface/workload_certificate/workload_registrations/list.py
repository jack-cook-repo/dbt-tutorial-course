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
"""The command to list Workload Registrations based on location."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.workload_certificate import client
from googlecloudsdk.calliope import base as calliope_base


class List(calliope_base.ListCommand):
  """List Workload Registration resources under a location.

  List Workload Registration resources under a location in a fleet.

  ## Examples

  To List Workload Registrations, run:

    $ {command} --location us-central1
  """

  @staticmethod
  def Args(parser):
    parser.add_argument(
        '--location',
        required=True,
        help='Location of workload registration.',
    )

  def Run(self, args):
    return client.WIPClient(self.ReleaseTrack()).ListRegistrations(
        args.location
    )
