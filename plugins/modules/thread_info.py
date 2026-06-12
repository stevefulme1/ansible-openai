#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r"""
---
module: thread_info
short_description: Retrieve information about thread resources
version_added: "1.0.0"
description:
  - Retrieve a single thread by its identifier, or list all thread resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the thread to retrieve.
      - When omitted, all thread resources are listed.
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
- name: Get a specific thread
  stevefulme1.openai.thread_info:
    id: "example_id"
  register: result

- name: List all thread resources
  stevefulme1.openai.thread_info:
  register: result

- name: List thread resources with pagination
  stevefulme1.openai.thread_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
threads:
  description: List of thread resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    id:
      description: >-
        The identifier, which can be referenced in API endpoints.
      type: str

    object:
      description: >-
        The object type, which is always thread.
      type: str

    created_at:
      description: >-
        The Unix timestamp (in seconds) for when the thread was created.
      type: int

    tool_resources:
      description: >-
        A set of resources that are made available to the assistant's tools in this thread. The...
      type: dict

    metadata:
      description: >-
        Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
      type: dict

"""

from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule


def fetch_single(client, identifier):
    """Retrieve a single thread by identifier."""

    raise ClientError("GET by identifier is not supported for this resource")


def fetch_list(client, module):
    """List thread resources with optional filtering and pagination."""

    raise ClientError("List operation is not supported for this resource")


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
        threads=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["threads"] = [item] if item else []
        else:
            result["threads"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
