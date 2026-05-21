#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: model_info
short_description: Retrieve information about model resources
version_added: "1.0.0"
description:
  - Retrieve a single model by its identifier, or list all model resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the model to retrieve.
      - When omitted, all model resources are listed.
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
- name: Get a specific model
  stevefulme1.openai.model_info:
    id: "example_id"
  register: result

- name: List all model resources
  stevefulme1.openai.model_info:
  register: result

- name: List model resources with pagination
  stevefulme1.openai.model_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
models:
  description: List of model resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    id:
      description: >-
        The model identifier, which can be referenced in the API endpoints.
      type: str

    created:
      description: >-
        The Unix timestamp (in seconds) when the model was created.
      type: int

    object:
      description: >-
        The object type, which is always "model".
      type: str

    owned_by:
      description: >-
        The organization that owns the model.
      type: str

"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)

def fetch_single(client, identifier):
    """Retrieve a single model by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/models")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None

def fetch_list(client, module):
    """List model resources with optional filtering and pagination."""

    params = {}

    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/models", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/models", params=params)

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
        models=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["models"] = [item] if item else []
        else:
            result["models"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

if __name__ == "__main__":
    main()
