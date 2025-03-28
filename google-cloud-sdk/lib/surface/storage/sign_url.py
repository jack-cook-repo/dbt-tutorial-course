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
"""Implementation of sign url command for Cloud Storage."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import textwrap

from googlecloudsdk.calliope import base


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class SignUrl(base.Command):
  """Generate a URL with embedded authentication that can be used by anyone."""

  detailed_help = {
      'DESCRIPTION':
          """
      *{command}* will generate a signed URL that embeds authentication data so
      the URL can be used by someone who does not have a Google account. Please
      see the [Signed URLs documentation](https://cloud.google.com/storage/docs/access-control/signed-urls)
      for background about signed URLs.

      Note, `{command}` does not support operations on sub-directories. For
      example, unless you have an object named `some-directory/` stored inside
      the bucket `some-bucket`, the following command returns an error:
      `{command} gs://some-bucket/some-directory/`.

      If you used service account credentials for authentication, you can
      replace `--private-key-file` with `--use-service-account` to use the
      system-managed private key directly. This avoids the need to download
      the private key file.
      """,
      'EXAMPLES':
          """
      To create a signed url for downloading an object valid for 10 minutes:

        $ {command} gs://my-bucket/file.txt --duration=10m --private-key-file=key.json

      To create a signed url that will bill to my-billing-project:

        $ {command} gs://my-bucket/file.txt --user-billing-project=my-billing-project --private-key-file=key.json

      To create a signed url without a private key, using a service account's
      credentials:

        $ {command} gs://my-bucket/file.txt --duration=10m --use-service-account

      To create a signed url by impersonating foo@developer.gserviceaccount.com:

        $ {command} gs://my-bucket/file.txt --duration=10m --use-service-account --impersonate-service-account=foo@developer.gserviceaccount.com

      To create a signed url, valid for one hour, for uploading a plain text
      file via HTTP PUT:

        $ {command} gs://my-bucket --method=PUT --duration=1h --content-type=text/plain --private-key-file=key.json
      """,
  }

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'url',
        nargs='+',
        help='The URLs to be signed. May contain wildcards.')
    parser.add_argument(
        '--private-key-file',
        help=textwrap.dedent("""\
            The service account private key used to generate the cryptographic
            signature for the generated URL. Must be in PKCS12 or JSON format.
            If encrypted, will prompt for the passphrase used to protect the
            private key file (default ``notasecret'')."""))
    parser.add_argument(
        '-b',
        '--user-billing-project',
        help=textwrap.dedent("""\
            Allows you to specify a user project that will be billed for
            requests that use the signed URL. This is useful for generating
            presigned links for buckets that use requester pays.

            Note that it's not valid to specify both `--user-billing-project`
            and `--use-service-account` options together."""))
    parser.add_argument(
        '-c',
        '--content-type',
        help=textwrap.dedent("""\
            Specifies the content type for which the signed url is valid
            for."""))
    parser.add_argument(
        '-d',
        '--duration',
        help=textwrap.dedent("""\
            Specifies the duration that the signed url should be valid for,
            default duration is 1 hour. For example 10s for 10 seconds.
            See $ gcloud topic datetimes for information on duration formats.

            The max duration allowed is 7 days when PRIVATE_KEY_FILE is used.

            The max duration allowed is 12 hours when `--use-service-account` is
            used. This limitation exists because the system-managed key used to
            sign the URL may not remain valid after 12 hours."""))
    parser.add_argument(
        '-m',
        '--method',
        help=textwrap.dedent("""\
            Specifies the HTTP method to be authorized for use with the signed
            URL, default is GET. You may also specify RESUMABLE to create a
            signed resumable upload start URL. When using a signed URL to start
            a resumable upload session, you will need to specify the
            ``x-goog-resumable:start'' header in the request or else signature
            validation will fail."""))
    parser.add_argument(
        '-p',
        '--private-key-password',
        help='Specify the private key password instead of prompting.')
    parser.add_argument(
        '-r',
        '--region',
        help=textwrap.dedent("""\
            Specifies the region in which the resources for which you are
            creating signed URLs are stored.

            Default value is ``auto'' which will cause {command} to fetch the
            region for the resource. When auto-detecting the region, the current
            user's credentials, not the credentials from PRIVATE_KEY_FILE,
            are used to fetch the bucket's metadata."""))
    parser.add_argument(
        '-u',
        '--use-service-account',
        action='store_true',
        help=textwrap.dedent("""\
            Use service account credentials instead of a private key file to
            sign the URL. Has a maximum allowed duration of 12 hours for a valid
            link."""))

  def Run(self, args):
    raise NotImplementedError
