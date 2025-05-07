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
"""Command for describing Cloud Run Integrations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.run.integrations import types_utils
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import flags as run_flags
from googlecloudsdk.command_lib.run.integrations import flags
from googlecloudsdk.command_lib.run.integrations import integration_printer
from googlecloudsdk.command_lib.run.integrations import run_apps_operations
from googlecloudsdk.core.resource import resource_printer


@base.ReleaseTracks(
    base.ReleaseTrack.ALPHA,
    base.ReleaseTrack.BETA)
class Describe(base.DescribeCommand):
  """Describe a Cloud Run Integration."""

  detailed_help = {
      'DESCRIPTION':
          """\
          {description}
          """,
      'EXAMPLES':
          """\
          To describe an integration

              $ {command} my-redis-integration

         """,
  }

  @classmethod
  def Args(cls, parser):
    """Set up arguments for this command.

    Args:
      parser: An argparse.ArgumentParser.
    """
    flags.AddNamePositionalArg(parser)
    resource_printer.RegisterFormatter(
        integration_printer.INTEGRATION_PRINTER_FORMAT,
        integration_printer.IntegrationPrinter,
        hidden=True)
    parser.display_info.AddFormat(
        integration_printer.INTEGRATION_PRINTER_FORMAT)

  def Run(self, args):
    """Describe an integration type."""
    release_track = self.ReleaseTrack()
    name = args.name
    conn_context = connection_context.GetConnectionContext(
        args, run_flags.Product.RUN_APPS, release_track)
    with run_apps_operations.Connect(conn_context, release_track) as client:
      resource_config = client.GetIntegration(name)
      latest_deployment = client.GetLatestDeployment(resource_config)
      resource_status = client.GetIntegrationStatus(name)
      integration_type = types_utils.GetIntegrationType(resource_config)

      return integration_printer.Record(
          name=name,
          region=conn_context.region,
          integration_type=integration_type,
          config=resource_config,
          status=resource_status,
          latest_deployment=latest_deployment,
      )
