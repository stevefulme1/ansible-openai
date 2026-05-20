#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: batch
short_description: Manage batch
version_added: "1.0.0"
description:
  - Create, update, and delete batch resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Auto-generated"
options:
  state:
    description:
      - Desired state of the batch resource.
    type: str
    choices: ['present', 'absent']
    default: present

  completion_window:
    description:
      - >-
        The time frame within which the batch should be processed. Currently only 24h is supported.
    type: str

    required: true


    choices: ["24h"]




  endpoint:
    description:
      - >-
        The endpoint to be used for all requests in the batch. Currently /v1/responses,...
    type: str

    required: true


    choices: ["/v1/responses", "/v1/chat/completions", "/v1/embeddings", "/v1/completions", "/v1/moderations", "/v1/images/generations", "/v1/images/edits", "/v1/videos"]




  input_file_id:
    description:
      - >-
        The ID of an uploaded file that contains requests for the new batch. See upload...
    type: str

    required: true





  metadata:
    description:
      - >-
        Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
    type: dict





  output_expires_after:
    description:
      - >-
        The expiration policy for the output and/or error file that are generated for a batch.
    type: dict





extends_documentation_fragment:
  - stevefulme1.openai.auth
"""

EXAMPLES = r"""

- name: Create a batch
  stevefulme1.openai.batch:


    completion_window: "example_completion_window"



    endpoint: "example_endpoint"



    input_file_id: "example_input_file_id"






    state: present
  # API: POST /batchs



- name: Update a batch
  stevefulme1.openai.batch:
    id: "existing_id"








    metadata: "updated_metadata"



    output_expires_after: "updated_output_expires_after"


    state: present
  # API:  



"""

RETURN = r"""

id:
  description: >-
    
  returned: success
  type: str


object:
  description: >-
    The object type, which is always batch.
  returned: success
  type: str


endpoint:
  description: >-
    The OpenAI API endpoint used by the batch.
  returned: success
  type: str


model:
  description: >-
    Model ID used to process the batch, like gpt-5-2025-08-07. OpenAI offers a wide range of models...
  returned: success
  type: str


errors:
  description: >-
    
  returned: success
  type: dict


input_file_id:
  description: >-
    The ID of the input file for the batch.
  returned: success
  type: str


completion_window:
  description: >-
    The time frame within which the batch should be processed.
  returned: success
  type: str


status:
  description: >-
    The current status of the batch.
  returned: success
  type: str


output_file_id:
  description: >-
    The ID of the file containing the outputs of successfully executed requests.
  returned: success
  type: str


error_file_id:
  description: >-
    The ID of the file containing the outputs of requests with errors.
  returned: success
  type: str


created_at:
  description: >-
    The Unix timestamp (in seconds) for when the batch was created.
  returned: success
  type: int


in_progress_at:
  description: >-
    The Unix timestamp (in seconds) for when the batch started processing.
  returned: success
  type: int


expires_at:
  description: >-
    The Unix timestamp (in seconds) for when the batch will expire.
  returned: success
  type: int


finalizing_at:
  description: >-
    The Unix timestamp (in seconds) for when the batch started finalizing.
  returned: success
  type: int


completed_at:
  description: >-
    The Unix timestamp (in seconds) for when the batch was completed.
  returned: success
  type: int


failed_at:
  description: >-
    The Unix timestamp (in seconds) for when the batch failed.
  returned: success
  type: int


expired_at:
  description: >-
    The Unix timestamp (in seconds) for when the batch expired.
  returned: success
  type: int


cancelling_at:
  description: >-
    The Unix timestamp (in seconds) for when the batch started cancelling.
  returned: success
  type: int


cancelled_at:
  description: >-
    The Unix timestamp (in seconds) for when the batch was cancelled.
  returned: success
  type: int


request_counts:
  description: >-
    The request counts for different statuses within the batch.
  returned: success
  type: dict


usage:
  description: >-
    Represents token usage details including input tokens, output tokens, a breakdown of output...
  returned: success
  type: dict


metadata:
  description: >-
    Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
  returned: success
  type: dict


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the batch via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    search_key = "id"
    search_value = identifier

    if search_value is None:
        return None
    try:
        items = client.get("/batchs")
        if isinstance(items, dict):
            items = items.get("results", items.get("data", items.get("items", [])))
        for item in items:
            if str(item.get(search_key)) == str(search_value):
                return item
            if str(item.get("id")) == str(search_value):
                return item
        return None
    except ClientError:
        return None



def needs_update(current, desired):
    """Compare current state against desired params and return True if an update is needed."""
    if current is None:
        return True
    for key, value in desired.items():
        if value is None:
            continue
        current_value = current.get(key)
        if current_value != value:
            return True
    return False


def build_payload(module):
    """Build the API request payload from module params."""
    payload = {}

    if module.params.get("completion_window") is not None:
        payload["completion_window"] = module.params["completion_window"]

    if module.params.get("endpoint") is not None:
        payload["endpoint"] = module.params["endpoint"]

    if module.params.get("input_file_id") is not None:
        payload["input_file_id"] = module.params["input_file_id"]

    if module.params.get("metadata") is not None:
        payload["metadata"] = module.params["metadata"]

    if module.params.get("output_expires_after") is not None:
        payload["output_expires_after"] = module.params["output_expires_after"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            completion_window=dict(
                type="str",

                required=True,


                choices=['24h'],




            ),

            endpoint=dict(
                type="str",

                required=True,


                choices=['/v1/responses', '/v1/chat/completions', '/v1/embeddings', '/v1/completions', '/v1/moderations', '/v1/images/generations', '/v1/images/edits', '/v1/videos'],




            ),

            input_file_id=dict(
                type="str",

                required=True,





            ),

            metadata=dict(
                type="dict",





            ),

            output_expires_after=dict(
                type="dict",





            ),

        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,

    )

    state = module.params["state"]
    result = dict(changed=False, diff=dict(before={}, after={}))

    try:
        client = Client(module)
        current = get_current_state(client, module)

        if state == "present":
            desired = build_payload(module)

            if current is None:
                # Resource does not exist — create it
                result["changed"] = True
                result["diff"]["before"] = {}
                result["diff"]["after"] = desired

                if not module.check_mode:

                    response = client.POST(
                        "/batchs",
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


            elif needs_update(current, desired):
                # Resource exists but needs updating
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = dict(current, **{k: v for k, v in desired.items() if v is not None})

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


            else:
                # Resource exists and is up-to-date

                result["id"] = current.get("id")

                result["object"] = current.get("object")

                result["endpoint"] = current.get("endpoint")

                result["model"] = current.get("model")

                result["errors"] = current.get("errors")

                result["input_file_id"] = current.get("input_file_id")

                result["completion_window"] = current.get("completion_window")

                result["status"] = current.get("status")

                result["output_file_id"] = current.get("output_file_id")

                result["error_file_id"] = current.get("error_file_id")

                result["created_at"] = current.get("created_at")

                result["in_progress_at"] = current.get("in_progress_at")

                result["expires_at"] = current.get("expires_at")

                result["finalizing_at"] = current.get("finalizing_at")

                result["completed_at"] = current.get("completed_at")

                result["failed_at"] = current.get("failed_at")

                result["expired_at"] = current.get("expired_at")

                result["cancelling_at"] = current.get("cancelling_at")

                result["cancelled_at"] = current.get("cancelled_at")

                result["request_counts"] = current.get("request_counts")

                result["usage"] = current.get("usage")

                result["metadata"] = current.get("metadata")


        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    pass


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
