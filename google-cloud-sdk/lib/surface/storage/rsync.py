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
"""Implementation of rsync command for Cloud Storage."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.storage import encryption_util
from googlecloudsdk.command_lib.storage import flags
from googlecloudsdk.command_lib.storage import rsync_command_util
from googlecloudsdk.command_lib.storage import user_request_args_factory
from googlecloudsdk.command_lib.storage.tasks import get_sorted_list_file_task
from googlecloudsdk.command_lib.storage.tasks import task_executor
from googlecloudsdk.command_lib.storage.tasks import task_graph_executor
from googlecloudsdk.command_lib.storage.tasks import task_status


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Rsync(base.Command):
  """Synchronize content of two buckets/directories."""

  detailed_help = {
      'DESCRIPTION': """
      *{command}* copies to and updates objects at `DESTINATION` to match
      `SOURCE`. `SOURCE` must specify a directory, bucket, or bucket
      subdirectory. *{command}* does not copy empty directory trees,
      since storage providers use a [flat namespace](https://cloud.google.com/storage/docs/folders).

      Note, shells (like bash, zsh) sometimes attempt to expand wildcards in
      ways that can be surprising. Also, attempting to copy files whose names
      contain wildcard characters can result in problems.

      If synchronizing a large amount of data between clouds you might consider
      setting up a Google Compute Engine account and running *{command}* there.
      Since *{command}* cross-provider data transfers flow through the machine
      where *{command}* is running, doing this can make your transfer run
      significantly faster than on your local workstation.

      """,
      'EXAMPLES': """
      To sync the contents of the local directory ``data'' to the bucket
      gs://my-bucket/data:

        $ {command} data gs://my-bucket/data
      """,
      # TODO(b/267511499): Code for rest of examples in bug.
  }

  @staticmethod
  def Args(parser):
    parser.add_argument('source', help='The source container path.')
    parser.add_argument('destination', help='The destination container path.')
    flags.add_encryption_flags(parser)
    # TODO(b/267511499): Code for unimplemented flags in bug.

  def Run(self, args):
    encryption_util.initialize_key_store(args)
    source_container = rsync_command_util.get_existing_container_resource(
        os.path.expanduser(args.source)
    )
    destination_container = (
        rsync_command_util.get_container_or_container_create_location_resource(
            os.path.expanduser(args.destination)
        )
    )

    # Create list tasks for source and destination and execute in parallel.
    source_list_path = rsync_command_util.get_hashed_list_file_path(
        source_container.storage_url.url_string
    )
    destination_list_path = rsync_command_util.get_hashed_list_file_path(
        destination_container.storage_url.url_string
    )
    source_task = get_sorted_list_file_task.GetSortedContainerContentsTask(
        source_container, source_list_path
    )
    destination_task = get_sorted_list_file_task.GetSortedContainerContentsTask(
        destination_container, destination_list_path
    )

    try:
      listing_exit_code = task_executor.execute_tasks(
          [source_task, destination_task], parallelizable=True
      )
      if listing_exit_code:
        return listing_exit_code

      user_request_args = (
          user_request_args_factory.get_user_request_args_from_command_args(
              args, metadata_type=user_request_args_factory.MetadataType.OBJECT
          )
      )
      # Execute a new task iterator for rsync copy, delete, and patch
      # operations iterating through the two sorted list files.
      operation_iterator = rsync_command_util.get_operation_iterator(
          user_request_args,
          source_list_path,
          source_container,
          destination_list_path,
          destination_container,
      )
      task_status_queue = task_graph_executor.multiprocessing_context.Queue()
      return task_executor.execute_tasks(
          operation_iterator,
          parallelizable=True,
          progress_manager_args=task_status.ProgressManagerArgs(
              task_status.IncrementType.FILES_AND_BYTES,
              manifest_path=user_request_args.manifest_path,
          ),
          task_status_queue=task_status_queue,
      )
    finally:
      rsync_command_util.try_to_delete_file(source_list_path)
      rsync_command_util.try_to_delete_file(destination_list_path)
