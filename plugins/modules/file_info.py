#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = r"""
---
module: file_info
short_description: Retrieve information about file resources
version_added: "1.0.0"
description:
  - Retrieve a single file by its identifier, or list all file resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the file to retrieve.
      - When omitted, all file resources are listed.
    type: str
    required: false

  page:
    description:
      - Page number for paginated results.
      - Only applies when listing resources.
    type: int
    required: false
  page_size:
    description:
      - Number of results per page.
      - Only applies when listing resources.
    type: int
    required: false
extends_documentation_fragment:
  - stevefulme1.openai.auth
"""

EXAMPLES = r"""
- name: Get a specific file
  stevefulme1.openai.file_info:
    id: "example_id"
  register: result

- name: List all file resources
  stevefulme1.openai.file_info:
  register: result

- name: List file resources with pagination
  stevefulme1.openai.file_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
files:
  description: List of file resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    id:
      description: >-
        The file identifier, which can be referenced in the API endpoints.
      type: str

    bytes:
      description: >-
        The size of the file, in bytes.
      type: int

    created_at:
      description: >-
        The Unix timestamp (in seconds) for when the file was created.
      type: int

    expires_at:
      description: >-
        The Unix timestamp (in seconds) for when the file will expire.
      type: int

    filename:
      description: >-
        The name of the file.
      type: str

    object:
      description: >-
        The object type, which is always file.
      type: str

    purpose:
      description: >-
        The intended purpose of the file. Supported values are assistants, assistants_output, batch,...
      type: str

    status:
      description: >-
        Deprecated. The current status of the file, which can be either uploaded, processed, or error.
      type: str

    status_details:
      description: >-
        Deprecated. For details on why a fine-tuning training file failed validation, see the error...
      type: str

"""


def fetch_single(client, identifier):
    """Retrieve a single file by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/files")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None


def fetch_list(client, module):
    """List file resources with optional filtering and pagination."""

    params = {}

    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/files", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/files", params=params)


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            id=dict(type="str", required=False),

            page=dict(type="int", required=False),
            page_size=dict(type="int", required=False),
        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ("id", "page"),
            ("id", "page_size"),
        ],
    )

    result = dict(
        changed=False,
        files=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["files"] = [item] if item else []
        else:
            result["files"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
