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
"""Implementation of Unix-like du command for cloud storage providers."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.storage import flags


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Du(base.Command):
  """Displays the amount of space in bytes used up storage resources."""

  detailed_help = {
      'DESCRIPTION':
          """
      Displays the amount of space in bytes used up by the objects in a bucket,
      subdirectory, or project.
      """,
      'EXAMPLES':
          """

      To list the size of each object in a bucket:

        $ {command} gs://bucketname

      To list the size of each object in the prefix subdirectory:

        $ {command} gs://bucketname/prefix/*

      To print the total number of bytes in a bucket in human-readable form:

        $ {command} -ch gs://bucketname

      To see a summary of the total number of bytes in two given buckets:

        $ {command} -s gs://bucket1 gs://bucket2

      To list the size of each object in a bucket with Object Versioning
      enabled, including noncurrent objects:

        $ {command} -a gs://bucketname

      To list the size of each object in a bucket, except objects that end in
      ".bak", with each object printed ending in a null byte:

        $ {command} -e "*.bak" -0 gs://bucketname

      To list the size of each bucket in a project and the total size of the
      project:

        $ {command} --only-total-size --human-readable --include-total-size
      """,
  }

  @staticmethod
  def Args(parser):
    parser.add_argument('url', nargs='+', help='The url of objects to list.')
    parser.add_argument(
        '--zero-terminator',
        action='store_true',
        help='Ends each output line with a 0 byte rather than a newline. You'
        ' can use this to make the output machine-readable.')
    parser.add_argument(
        '-a',
        '--all-versions',
        action='store_true',
        help='Includes noncurrent object versions for a bucket with Object'
        ' Versioning enabled. Also prints the generation and metageneration'
        ' number for each listed object.')
    parser.add_argument(
        '-c',
        '--include-total-size',
        action='store_true',
        help='Includes a total size at the end of the output.')
    parser.add_argument(
        '-e',
        '--exclude-name-pattern',
        action='store_true',
        help='Exclude a pattern from the report. Example: -e "*.o" excludes any'
        ' object that ends in ".o". Can be specified multiple times.')
    parser.add_argument(
        '--human-readable',
        action='store_true',
        help='Prints object sizes in human-readable format. For example, 1 KiB,'
        ' 234 MiB, or 2GiB.')
    parser.add_argument(
        '-s',
        '--only-total-size',
        action='store_true',
        help='Displays only the total size for each argument.')
    parser.add_argument(
        '-X',
        '--exclude-content-pattern',
        action='store_true',
        help='Similar to -e, but excludes patterns from the given file.'
        ' The patterns to exclude should be listed one per line.')

    flags.add_additional_headers_flag(parser)

  def Run(self, args):
    del args  # Unused.
    raise NotImplementedError
