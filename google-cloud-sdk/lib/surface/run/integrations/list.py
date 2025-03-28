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
"""Command for listing Cloud Run Integrations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.run.integrations import types_utils
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import flags as run_flags
from googlecloudsdk.command_lib.run.integrations import flags
from googlecloudsdk.command_lib.run.integrations import integration_list_printer as printer
from googlecloudsdk.command_lib.run.integrations import run_apps_operations
from googlecloudsdk.core.resource import resource_printer


@base.ReleaseTracks(
    base.ReleaseTrack.ALPHA,
    base.ReleaseTrack.BETA)
class List(base.ListCommand):
  """List Cloud Run Integrations."""

  detailed_help = {
      'DESCRIPTION':
          """\
          {description}
          """,
      'EXAMPLES':
          """\
          List all Cloud Run Integrations within the current project

              $ {command}

          List all Cloud Run Integrations of a particular type

              $ {command} --type=redis

          List all Cloud Run Integrations attached to a particular Service

              $ {command} --service=my-service

         """,
  }

  @classmethod
  def Args(cls, parser):
    """Set up arguments for this command.

    Args:
      parser: An argparse.ArgumentParser.
    """
    flags.ListIntegrationsOfService(parser)
    flags.ListIntegrationsOfType(parser)

    resource_printer.RegisterFormatter(
        printer.PRINTER_FORMAT,
        printer.IntegrationListPrinter,
        hidden=True,
    )
    parser.display_info.AddFormat(printer.PRINTER_FORMAT)

  def Run(self, args):
    """Lists all the Cloud Run Integrations.

    Args:
      args: ArgumentParser, used to reference the inputs provided by the user.

    Returns:
      dict with a single key that maps to a list of integrations.
      This will be used by the integration_list_printer to format all
      the entries in the list.

      The reason this is not a list is because the printer will only recieve
      one entry at a time and cannot easily format all entries into a table.
    """
    integration_type = args.type
    service_name = args.service
    release_track = self.ReleaseTrack()

    conn_context = connection_context.GetConnectionContext(
        args, run_flags.Product.RUN_APPS, release_track)
    with run_apps_operations.Connect(conn_context, release_track) as client:
      if integration_type:
        types_utils.CheckValidIntegrationType(integration_type)

      return {
          printer.RECORD_KEY:
              client.ListIntegrations(integration_type, service_name)
          }
