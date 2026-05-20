#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: batch_info
short_description: Retrieve information about batch resources
version_added: "1.0.0"
description:
  - Retrieve a single batch by its identifier, or list all batch resources.
  - This module always reports C(changed=False).
author:
  - "Auto-generated"
options:
  id:
    description:
      - The unique identifier of the batch to retrieve.
      - When omitted, all batch resources are listed.
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
- name: Get a specific batch
  stevefulme1.openai.batch_info:
    id: "example_id"
  register: result

- name: List all batch resources
  stevefulme1.openai.batch_info:
  register: result



- name: List batch resources with pagination
  stevefulme1.openai.batch_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
batchs:
  description: List of batch resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    id:
      description: >-
        
      type: str


    object:
      description: >-
        The object type, which is always batch.
      type: str


    endpoint:
      description: >-
        The OpenAI API endpoint used by the batch.
      type: str


    model:
      description: >-
        Model ID used to process the batch, like gpt-5-2025-08-07. OpenAI offers a wide range of models...
      type: str


    errors:
      description: >-
        
      type: dict


    input_file_id:
      description: >-
        The ID of the input file for the batch.
      type: str


    completion_window:
      description: >-
        The time frame within which the batch should be processed.
      type: str


    status:
      description: >-
        The current status of the batch.
      type: str


    output_file_id:
      description: >-
        The ID of the file containing the outputs of successfully executed requests.
      type: str


    error_file_id:
      description: >-
        The ID of the file containing the outputs of requests with errors.
      type: str


    created_at:
      description: >-
        The Unix timestamp (in seconds) for when the batch was created.
      type: int


    in_progress_at:
      description: >-
        The Unix timestamp (in seconds) for when the batch started processing.
      type: int


    expires_at:
      description: >-
        The Unix timestamp (in seconds) for when the batch will expire.
      type: int


    finalizing_at:
      description: >-
        The Unix timestamp (in seconds) for when the batch started finalizing.
      type: int


    completed_at:
      description: >-
        The Unix timestamp (in seconds) for when the batch was completed.
      type: int


    failed_at:
      description: >-
        The Unix timestamp (in seconds) for when the batch failed.
      type: int


    expired_at:
      description: >-
        The Unix timestamp (in seconds) for when the batch expired.
      type: int


    cancelling_at:
      description: >-
        The Unix timestamp (in seconds) for when the batch started cancelling.
      type: int


    cancelled_at:
      description: >-
        The Unix timestamp (in seconds) for when the batch was cancelled.
      type: int


    request_counts:
      description: >-
        The request counts for different statuses within the batch.
      type: dict


    usage:
      description: >-
        Represents token usage details including input tokens, output tokens, a breakdown of output...
      type: dict


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
    """Retrieve a single batch by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/batchs")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List batch resources with optional filtering and pagination."""

    params = {}















    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/batchs", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/batchs", params=params)



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
        batchs=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["batchs"] = [item] if item else []
        else:
            result["batchs"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
