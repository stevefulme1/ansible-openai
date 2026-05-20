#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: fine_tuning_job_info
short_description: Retrieve information about fine_tuning_job resources
version_added: "1.0.0"
description:
  - Retrieve a single fine_tuning_job by its identifier, or list all fine_tuning_job resources.
  - This module always reports C(changed=False).
author:
  - "Auto-generated"
options:
  id:
    description:
      - The unique identifier of the fine_tuning_job to retrieve.
      - When omitted, all fine_tuning_job resources are listed.
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
- name: Get a specific fine_tuning_job
  stevefulme1.openai.fine_tuning_job_info:
    id: "example_id"
  register: result

- name: List all fine_tuning_job resources
  stevefulme1.openai.fine_tuning_job_info:
  register: result



- name: List fine_tuning_job resources with pagination
  stevefulme1.openai.fine_tuning_job_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
fine_tuning_jobs:
  description: List of fine_tuning_job resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    id:
      description: >-
        The object identifier, which can be referenced in the API endpoints.
      type: str


    created_at:
      description: >-
        The Unix timestamp (in seconds) for when the fine-tuning job was created.
      type: int


    error:
      description: >-
        For fine-tuning jobs that have failed, this will contain more information on the cause of the failure.
      type: dict


    fine_tuned_model:
      description: >-
        The name of the fine-tuned model that is being created. The value will be null if the...
      type: str


    finished_at:
      description: >-
        The Unix timestamp (in seconds) for when the fine-tuning job was finished. The value will be...
      type: int


    hyperparameters:
      description: >-
        The hyperparameters used for the fine-tuning job. This value will only be returned when running...
      type: dict


    model:
      description: >-
        The base model that is being fine-tuned.
      type: str


    object:
      description: >-
        The object type, which is always "fine_tuning.job".
      type: str


    organization_id:
      description: >-
        The organization that owns the fine-tuning job.
      type: str


    result_files:
      description: >-
        The compiled results file ID(s) for the fine-tuning job. You can retrieve the results with the...
      type: list


    status:
      description: >-
        The current status of the fine-tuning job, which can be either validating_files, queued,...
      type: str


    trained_tokens:
      description: >-
        The total number of billable tokens processed by this fine-tuning job. The value will be null if...
      type: int


    training_file:
      description: >-
        The file ID used for training. You can retrieve the training data with the Files...
      type: str


    validation_file:
      description: >-
        The file ID used for validation. You can retrieve the validation results with the Files...
      type: str


    integrations:
      description: >-
        A list of integrations to enable for this fine-tuning job.
      type: list


    seed:
      description: >-
        The seed used for the fine-tuning job.
      type: int


    estimated_finish:
      description: >-
        The Unix timestamp (in seconds) for when the fine-tuning job is estimated to finish. The value...
      type: int


    method:
      description: >-
        The method used for fine-tuning.
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
    """Retrieve a single fine_tuning_job by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/fine_tuning/jobs")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("id")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List fine_tuning_job resources with optional filtering and pagination."""

    params = {}























    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/fine_tuning/jobs", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/fine_tuning/jobs", params=params)



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
        fine_tuning_jobs=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["fine_tuning_jobs"] = [item] if item else []
        else:
            result["fine_tuning_jobs"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
