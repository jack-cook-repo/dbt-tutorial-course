#!/usr/bin/env python
"""A library of functions to handle bq flags consistently."""

import codecs
import http.client
import json
import logging
import os
import pkgutil
import platform
import sys
import textwrap
import time
import traceback

from absl import app
from absl import flags
import googleapiclient
import httplib2
import oauth2client_4_0.client
import six

import bigquery_client

FLAGS = flags.FLAGS

_GDRIVE_SCOPE = 'https://www.googleapis.com/auth/drive'
_BIGQUERY_SCOPE = 'https://www.googleapis.com/auth/bigquery'
_CLOUD_PLATFORM_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'
_REAUTH_SCOPE = 'https://www.googleapis.com/auth/accounts.reauth'


_BIGQUERY_TOS_MESSAGE = (
    'In order to get started, please visit the Google APIs Console to '
    'create a project and agree to our Terms of Service:\n'
    '\thttps://console.cloud.google.com/\n\n'
    'For detailed sign-up instructions, please see our Getting Started '
    'Guide:\n'
    '\thttps://cloud.google.com/bigquery/docs/quickstarts/'
    'quickstart-command-line\n\n'
    'Once you have completed the sign-up process, please try your command '
    'again.')
_VERSION_FILENAME = 'VERSION'


def _GetVersion():
  """Returns content of VERSION file found in same dir as the cli binary."""
  root = 'bq_utils'
  return six.ensure_str(pkgutil.get_data(root, _VERSION_FILENAME)).strip()


VERSION_NUMBER = _GetVersion()


def GetBigqueryRcFilename():
  """Return the name of the bigqueryrc file to use.

  In order, we look for a flag the user specified, an environment
  variable, and finally the default value for the flag.

  Returns:
    bigqueryrc filename as a string.
  """
  return ((FLAGS['bigqueryrc'].present and FLAGS.bigqueryrc) or
          os.environ.get('BIGQUERYRC') or FLAGS.bigqueryrc)


def ProcessBigqueryrc():
  """Updates FLAGS with values found in the bigqueryrc file."""
  ProcessBigqueryrcSection(None, FLAGS)


def ProcessBigqueryrcSection(section_name, flag_values):
  """Read the bigqueryrc file into flag_values for section section_name.

  Args:
    section_name: if None, read the global flag settings.
    flag_values: FLAGS instance.

  Raises:
    UsageError: Unknown flag found.
  """

  bigqueryrc = GetBigqueryRcFilename()
  if not os.path.exists(bigqueryrc):
    return
  with open(bigqueryrc) as rcfile:
    in_section = not section_name
    for line in rcfile:
      if line.lstrip().startswith('[') and line.rstrip().endswith(']'):
        next_section = line.strip()[1:-1]
        in_section = section_name == next_section
        continue
      elif not in_section:
        continue
      elif line.lstrip().startswith('#') or not line.strip():
        continue
      flag, equalsign, value = line.partition('=')
      # if no value given, assume stringified boolean true
      if not equalsign:
        value = 'true'
      flag = flag.strip()
      value = value.strip()
      while flag.startswith('-'):
        flag = flag[1:]
      # We want flags specified at the command line to override
      # those in the flagfile.
      if flag not in flag_values:
        raise app.UsageError(
            'Unknown flag %s found in bigqueryrc file in section %s' %
            (flag, section_name if section_name else 'global'))
      if not flag_values[flag].present:
        # This updates the .value and .present attributes.
        flag_values[flag].parse(value)
        # This updates the .using_default_value attribute in addition.
        setattr(flag_values, flag, getattr(flag_values, flag))
      else:
        flag_type = flag_values[flag].flag_type()
        if flag_type.startswith('multi'):
          old_value = getattr(flag_values, flag)
          flag_values[flag].parse(value)
          setattr(flag_values, flag, old_value + getattr(flag_values, flag))


def ProcessError(
    err,
    name='unknown',
    message_prefix='You have encountered a bug in the BigQuery CLI.'):
  """Translate an error message into some printing and a return code."""

  logger = logging.getLogger(__name__)

  if isinstance(err, SystemExit):
    logger.exception('An error has caused the tool to exit', exc_info=err)
    return err.code  # sys.exit called somewhere, hopefully intentionally.

  response = []
  retcode = 1

  (etype, value, tb) = sys.exc_info()
  trace = ''.join(traceback.format_exception(etype, value, tb))
  # pragma pylint: disable=line-too-long
  contact_us_msg = (
      'Please file a bug report in our '
      'public '
      'issue tracker:\n'
      '  https://issuetracker.google.com/issues/new?component=187149&template=0\n'
      'Please include a brief description of '
      'the steps that led to this issue, as well as '
      'any rows that can be made public from '
      'the following information: \n\n')
  platform_str = ':'.join([
      platform.python_implementation(),
      platform.python_version(),
      platform.platform()
  ])
  error_details = textwrap.dedent("""\
     ========================================
     == Platform ==
       %s
     == bq version ==
       %s
     == Command line ==
       %s
     == UTC timestamp ==
       %s
     == Error trace ==
     %s
     ========================================
     """) % (
         platform_str,
         six.ensure_str(VERSION_NUMBER),
         [six.ensure_str(item) for item in sys.argv],
         time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
         six.ensure_str(trace))

  codecs.register_error('strict', codecs.replace_errors)
  message = bigquery_client.EncodeForPrinting(err)
  if isinstance(err, (bigquery_client.BigqueryNotFoundError,
                      bigquery_client.BigqueryDuplicateError)):
    response.append('BigQuery error in %s operation: %s' % (name, message))
    retcode = 2
  elif isinstance(err, bigquery_client.BigqueryTermsOfServiceError):
    response.append(str(err) + '\n')
    response.append(_BIGQUERY_TOS_MESSAGE)
  elif isinstance(err, bigquery_client.BigqueryInvalidQueryError):
    response.append('Error in query string: %s' % (message,))
  elif (isinstance(err, bigquery_client.BigqueryError) and
        not isinstance(err, bigquery_client.BigqueryInterfaceError)):
    response.append('BigQuery error in %s operation: %s' % (name, message))
  elif isinstance(err, (app.UsageError, TypeError)):
    response.append(message)
  elif (isinstance(err, SyntaxError) or
        isinstance(err, bigquery_client.BigquerySchemaError)):
    response.append('Invalid input: %s' % (message,))
  elif isinstance(err, flags.Error):
    response.append('Error parsing command: %s' % (message,))
  elif isinstance(err, KeyboardInterrupt):
    response.append('')
  else:  # pylint: disable=broad-except
    # Errors with traceback information are printed here.
    # The traceback module has nicely formatted the error trace
    # for us, so we don't want to undo that via TextWrap.
    if isinstance(err, bigquery_client.BigqueryInterfaceError):
      message_prefix = (
          'Bigquery service returned an invalid reply in %s operation: %s.'
          '\n\n'
          'Please make sure you are using the latest version '
          'of the bq tool and try again. '
          'If this problem persists, you may have encountered a bug in the '
          'bigquery client.' % (name, message))
    elif isinstance(err, oauth2client_4_0.client.Error):
      message_prefix = (
          'Authorization error. This may be a network connection problem, '
          'so please try again. If this problem persists, the credentials '
          'may be corrupt. Try deleting and re-creating your credentials. '
          'You can delete your credentials using '
          '"bq init --delete_credentials".'
          '\n\n'
          'If this problem still occurs, you may have encountered a bug '
          'in the bigquery client.')
    elif (isinstance(err, http.client.HTTPException) or
          isinstance(err, googleapiclient.errors.Error) or
          isinstance(err, httplib2.HttpLib2Error)):
      message_prefix = (
          'Network connection problem encountered, please try again.'
          '\n\n'
          'If this problem persists, you may have encountered a bug in the '
          'bigquery client.')

    message = message_prefix + ' ' + contact_us_msg
    wrap_error_message = True
    if wrap_error_message:
      message = flags.text_wrap(message)
    print(message)
    print(error_details)
    response.append('Unexpected exception in %s operation: %s' %
                    (name, message))

  response_message = '\n'.join(response)
  wrap_error_message = True
  if wrap_error_message:
    response_message = flags.text_wrap(response_message)
  logger.exception(response_message, exc_info=err)
  print(response_message)
  return retcode


def PrintFormattedJsonObject(obj, default_format='json'):
  """Prints obj in a JSON format according to the "--format" flag.

  Args:
    obj: The object to print.
    default_format: The format to use if the "--format" flag does not specify a
      valid json format: 'json' or 'prettyjson'.
  """
  json_formats = ['json', 'prettyjson']
  if FLAGS.format in json_formats:
    use_format = FLAGS.format
  else:
    use_format = default_format

  if use_format == 'json':
    print(json.dumps(obj, separators=(',', ':')))
  elif use_format == 'prettyjson':
    print(json.dumps(obj, sort_keys=True, indent=2))
  else:
    raise ValueError(
        'Invalid json format for printing: \'%s\', expected one of: %s' %
        (use_format, json_formats))


def GetClientScopeFromFlags():
  """Returns auth scopes based on user supplied flags."""
  client_scope = [_BIGQUERY_SCOPE, _CLOUD_PLATFORM_SCOPE]
  if FLAGS.enable_gdrive:
    client_scope.append(_GDRIVE_SCOPE)
  client_scope.append(_REAUTH_SCOPE)
  return client_scope


def GetClientScopesFor3pi():
  return [_CLOUD_PLATFORM_SCOPE]
