#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vector_store_info
short_description: Retrieve information about vector_store resources
version_added: "1.0.0"
description:
  - Retrieve a single vector_store by its identifier, or list all vector_store resources.
  - This module always reports C(changed=False).
author:
  - "Auto-generated"
options:
  id:
    description:
      - The unique identifier of the vector_store to retrieve.
      - When omitted, all vector_store resources are listed.
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
- name: Get a specific vector_store
  stevefulme1.openai.vector_store_info:
    id: "example_id"
  register: result

- name: List all vector_store resources
  stevefulme1.openai.vector_store_info:
  register: result


- name: List vector_store resources filtered by name
  stevefulme1.openai.vector_store_info:
    name: "my_vector_store"
  register: result


- name: List vector_store resources with pagination
  stevefulme1.openai.vector_store_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
vector_stores:
  description: List of vector_store resources matching the query.
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
        The object type, which is always vector_store.
      type: str


    created_at:
      description: >-
        The Unix timestamp (in seconds) for when the vector store was created.
      type: int


    name:
      description: >-
        The name of the vector store.
      type: str


    usage_bytes:
      description: >-
        The total number of bytes used by the files in the vector store.
      type: int


    file_counts:
      description: >-
        
      type: dict


    status:
      description: >-
        The status of the vector store, which can be either expired, in_progress, or completed. A status...
      type: str


    expires_after:
      description: >-
        The expiration policy for a vector store.
      type: dict


    expires_at:
      description: >-
        The Unix timestamp (in seconds) for when the vector store will expire.
      type: int


    last_active_at:
      description: >-
        The Unix timestamp (in seconds) for when the vector store was last active.
      type: int


    metadata:
      description: >-
        Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
      type: dict


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single vector_store by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/vector_stores")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List vector_store resources with optional filtering and pagination."""

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
        response = client.get("/vector_stores", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/vector_stores", params=params)



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
        vector_stores=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["vector_stores"] = [item] if item else []
        else:
            result["vector_stores"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
