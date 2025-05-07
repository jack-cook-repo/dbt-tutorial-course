#!/usr/bin/env python
"""Methods for loading discovery documents for Google Cloud APIs.

Discovery Documents are used to create API Clients.
"""

import pkgutil
import string
from absl import logging

FULL_PKG_NAME = 'bigquery_client'
SHORT_PKG_NAME = 'bigquery_client'

# Latest version of the BigQuery API discovery_document from discovery_next.
DISCOVERY_NEXT_BIGQUERY = 'discovery_next/bigquery.json'
# Latest version of the IAM Policy API discovery_document from discovery_next.
DISCOVERY_NEXT_IAM_POLICY = 'discovery_next/iam-policy.json'


def get_discovery_bigquery_name(api_url, api_version):
  """Returns a filename for `api_url` for fetching discovery doc from pkg files.

  Used for discovery and not discovery_next.

  Args:
    api_url: [str], The url for the discovery doc.
    api_version: [str], the version of the discovery doc.
  """
  filename_from_url = ''.join(
      [c for c in api_url if c in string.ascii_lowercase])
  doc_filename = 'discovery/{}.bigquery.{}.rest.json'.format(
      filename_from_url, api_version)
  return doc_filename


def load_local_discovery_doc(doc_filename):
  """Loads the discovery document for `doc_filename` with `version` from package files.

  Example:
    bq_disc_doc = discovery_document_loader
      .load_local_discovery_doc('discovery_next/bigquery.json')

  Args:
    doc_filename: [str], The filename of the discovery document to be loaded.

  Raises:
    FileNotFoundError: If no discovery doc could be loaded.

  Returns:
    `bytes`, On success, A json object with the contents of the
    discovery document. On failure, None.
  """
  doc = _fetch_discovery_doc_from_pkg(
      FULL_PKG_NAME, doc_filename) or _fetch_discovery_doc_from_pkg(
          SHORT_PKG_NAME, doc_filename)

  if not doc:
    raise FileNotFoundError(
        'Failed to load discovery doc from resource paths: %s.%s & %s.%s' %
        (FULL_PKG_NAME, doc_filename, SHORT_PKG_NAME, doc_filename))

  return doc


def _fetch_discovery_doc_from_pkg(package, resource):
  """Loads a discovery doc as `bytes` specified by `package` and `resource` returning None on error."""
  raw_doc = pkgutil.get_data(package, resource)
  if not raw_doc:
    logging.warning(
        'Failed to load discovery doc from pkg: package: %s, resource %s',
        package, resource)
  return raw_doc
