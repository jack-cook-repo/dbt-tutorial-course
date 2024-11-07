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

"""Command to provision a new Spectrum Access System's deployment."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.spectrum_access import sas_portal_api
from googlecloudsdk.calliope import base


@base.Hidden
class Provision(base.DescribeCommand):
  """Provision a new Spectrum Access System's deployment.

  ## EXAMPLES

  The following command provisions a new SAS deployment:

    $ gcloud spectrum-access provision --organization-name=MyOrgName
    --deployment-name=MyDeploymentName
  """

  @staticmethod
  def Args(parser):
    parser.add_argument(
        '--organization-name',
        required=False,
        help=(
            'The display name to use in case a new SAS Portal organization'
            ' needs to be created. If not set, a default display name of the'
            ' form "Cloud organizations/[ID]" will be used where ID is the'
            ' current Cloud Platform Organization ID.'
        ),
    )
    parser.add_argument(
        '--deployment-name',
        required=False,
        help=(
            'The display name to use in case a new SAS Portal deployment needs'
            ' to be created. If not set, a default display name of the form'
            ' "Cloud [ID]" will be used where ID is the current Cloud Platform'
            ' Project ID.'
        ),
    )

  def Run(self, args):
    base.EnableUserProjectQuota()
    client = sas_portal_api.GetClientInstance().customers
    messsage_module = sas_portal_api.GetMessagesModule()
    req = messsage_module.SasPortalProvisionDeploymentRequest()
    req.newOrganizationDisplayName = args.organization_name
    req.newDeploymentDisplayName = args.deployment_name
    return client.ProvisionDeployment(req)
