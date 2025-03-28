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

"""Command to list notification configurations belonging to a bucket."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.storage import notification_configuration_iterator
from googlecloudsdk.core.resource import resource_projector


class List(base.ListCommand):
  """List the notification configurations belonging to a given bucket."""

  detailed_help = {
      'DESCRIPTION':
          """
      *{command}* provides a list of notification configurations belonging to a
      given bucket. The listed name of each configuration can be used
      with the delete sub-command to delete that specific notification config.
      """,
      'EXAMPLES':
          """
      Fetch the list of notification configs for the bucket `example-bucket`:

        $ {command} gs://example-bucket

      Fetch the notification configs in all buckets matching a wildcard:

        $ {command} gs://example-*

      Fetch all of the notification configs for buckets in the default project:

        $ {command}
      """,
  }

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'urls',
        nargs='*',
        help='Google Cloud Storage bucket paths. The path must begin '
        'with gs:// and may contain wildcard characters.')

  def Run(self, args):
    if not args.urls:
      # Provider URL will fetch all notification configurations in project.
      urls = ['gs://']
    else:
      urls = args.urls

    # Not bucket URLs raise error in iterator.
    for notification_configuration_iterator_result in (
        notification_configuration_iterator
        .get_notification_configuration_iterator(
            urls, accept_notification_configuration_urls=False)):
      yield {
          'Bucket URL':
              notification_configuration_iterator_result.bucket_url.url_string,
          'Notification Configuration':
              resource_projector.MakeSerializable(
                  notification_configuration_iterator_result
                  .notification_configuration)
      }
