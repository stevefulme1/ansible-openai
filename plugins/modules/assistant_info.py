#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r"""
---
module: assistant_info
short_description: Retrieve information about assistant resources
version_added: "1.0.0"
description:
  - Retrieve a single assistant by its identifier, or list all assistant resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the assistant to retrieve.
      - When omitted, all assistant resources are listed.
    type: str
    required: false

  name:
    description:
      - Filter results by name.
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
- name: Get a specific assistant
  stevefulme1.openai.assistant_info:
    id: "example_id"
  register: result

- name: List all assistant resources
  stevefulme1.openai.assistant_info:
  register: result

- name: List assistant resources filtered by name
  stevefulme1.openai.assistant_info:
    name: "my_assistant"
  register: result

- name: List assistant resources with pagination
  stevefulme1.openai.assistant_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
assistants:
  description: List of assistant resources matching the query.
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
        The object type, which is always assistant.
      type: str

    created_at:
      description: >-
        The Unix timestamp (in seconds) for when the assistant was created.
      type: int

    name:
      description: >-
        The name of the assistant. The maximum length is 256 characters.
      type: str

    description:
      description: >-
        The description of the assistant. The maximum length is 512 characters.
      type: str

    model:
      description: >-
        ID of the model to use. You can use the List models(/docs/api-reference/models/list) API to see...
      type: str

    instructions:
      description: >-
        The system instructions that the assistant uses. The maximum length is 256,000 characters.
      type: str

    tools:
      description: >-
        A list of tool enabled on the assistant. There can be a maximum of 128 tools per assistant....
      type: list

    tool_resources:
      description: >-
        A set of resources that are used by the assistant's tools. The resources are specific to the...
      type: dict

    metadata:
      description: >-
        Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
      type: dict

    temperature:
      description: >-
        What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output...
      type: float

    top_p:
      description: >-
        An alternative to sampling with temperature, called nucleus sampling, where the model considers...
      type: float

    response_format:
      description: >-
        auto is the default value
      type: str

"""

from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule


def fetch_single(client, identifier):
    """Retrieve a single assistant by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/assistants")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None


def fetch_list(client, module):
    """List assistant resources with optional filtering and pagination."""

    params = {}

    name_filter = module.params.get("name")
    if name_filter is not None:
        params["name"] = name_filter

    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/assistants", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/assistants", params=params)


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            id=dict(type="str", required=False),

            name=dict(type="str", required=False),

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
        assistants=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["assistants"] = [item] if item else []
        else:
            result["assistants"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
