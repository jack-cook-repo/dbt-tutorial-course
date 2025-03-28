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
"""The command to enable Workload Certificate Feature."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.workload_certificate import client
from googlecloudsdk.calliope import base as calliope_base
from googlecloudsdk.command_lib.workload_certificate import resource


class Enable(calliope_base.UpdateCommand):
  """Enable Workload Certificate Feature.

  Enable the Workload Certificate Feature for a fleet project, specify
  mode=managed_ca to use managed CA.

  ## Examples

  To enable Workload Certificate Feature with managed CA, run:

    $ {command} --mode=managed_ca
  """

  @staticmethod
  def Args(parser):
    parser.add_argument(
        '--mode',
        choices=['managed_ca'],
        help=(
            '"managed_ca" enables Google managed CAS. By enabling managed CA, '
            'the entire certificate provisioning process is managed by Google, '
            'including the CA.'
        ),
    )

  def Run(self, args):
    if args.mode != 'managed_ca':
      raise Exception(
          '--mode=managed_ca must be set to enable workload certificate'
          ' feature.'
      )

    feature_name = resource.WorkloadCertificateFeatureResourceName(
        resource.Project()
    )
    return client.WIPClient(self.ReleaseTrack()).EnableFeature(feature_name)
