#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: assistant
short_description: Manage assistants
version_added: "1.0.0"
description:
  - Create, update, and delete assistant resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the assistant resource.
    type: str
    choices: ['present', 'absent']
    default: present

  description:
    description:
      - >-
        The description of the assistant. The maximum length is 512 characters.
    type: str

  instructions:
    description:
      - >-
        The system instructions that the assistant uses. The maximum length is 256,000 characters.
    type: str

  metadata:
    description:
      - >-
        Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
    type: dict

  model:
    description:
      - >-

    type: str

  name:
    description:
      - >-
        The name of the assistant. The maximum length is 256 characters.
    type: str

  reasoning_effort:
    description:
      - >-
        Constrains effort on reasoning for reasoning models. Currently supported values are none,...
    type: str

    choices: ["none", "minimal", "low", "medium", "high", "xhigh"]

    default: "medium"

  response_format:
    description:
      - >-
        auto is the default value
    type: str

    choices: ["auto"]

  temperature:
    description:
      - >-
        What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output...
    type: float

    default: 1

  tool_resources:
    description:
      - >-
        A set of resources that are used by the assistant's tools. The resources are specific to the...
    type: dict

  tools:
    description:
      - >-
        A list of tool enabled on the assistant. There can be a maximum of 128 tools per assistant....
    type: list
    elements: dict

    default: []

  top_p:
    description:
      - >-
        An alternative to sampling with temperature, called nucleus sampling, where the model considers...
    type: float

    default: 1

extends_documentation_fragment:
  - stevefulme1.openai.auth
"""

EXAMPLES = r"""

- name: Create a assistant
  stevefulme1.openai.assistant:

    state: present
  # API: POST /assistants/{assistant_id}

- name: Update a assistant
  stevefulme1.openai.assistant:
    id: "existing_id"

    description: "updated_description"

    instructions: "updated_instructions"

    metadata: "updated_metadata"

    model: "updated_model"

    name: "updated_name"

    reasoning_effort: "updated_reasoning_effort"

    response_format: "updated_response_format"

    temperature: "updated_temperature"

    tool_resources: "updated_tool_resources"

    tools: "updated_tools"

    top_p: "updated_top_p"

    state: present
  # API:

- name: Delete a assistant
  stevefulme1.openai.assistant:
    id: "existing_id"
    state: absent
  # API: DELETE /assistants/{assistant_id}

"""

RETURN = r"""

id:
  description: >-
    The identifier, which can be referenced in API endpoints.
  returned: success
  type: str

object:
  description: >-
    The object type, which is always assistant.
  returned: success
  type: str

created_at:
  description: >-
    The Unix timestamp (in seconds) for when the assistant was created.
  returned: success
  type: int

name:
  description: >-
    The name of the assistant. The maximum length is 256 characters.
  returned: success
  type: str

description:
  description: >-
    The description of the assistant. The maximum length is 512 characters.
  returned: success
  type: str

model:
  description: >-
    ID of the model to use. You can use the List models(/docs/api-reference/models/list) API to see...
  returned: success
  type: str

instructions:
  description: >-
    The system instructions that the assistant uses. The maximum length is 256,000 characters.
  returned: success
  type: str

tools:
  description: >-
    A list of tool enabled on the assistant. There can be a maximum of 128 tools per assistant....
  returned: success
  type: list

tool_resources:
  description: >-
    A set of resources that are used by the assistant's tools. The resources are specific to the...
  returned: success
  type: dict

metadata:
  description: >-
    Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
  returned: success
  type: dict

temperature:
  description: >-
    What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output...
  returned: success
  type: float

top_p:
  description: >-
    An alternative to sampling with temperature, called nucleus sampling, where the model considers...
  returned: success
  type: float

response_format:
  description: >-
    auto is the default value
  returned: success
  type: str

"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)

def get_current_state(client, module):
    """Retrieve the current state of the assistant via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/assistants")
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

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("instructions") is not None:
        payload["instructions"] = module.params["instructions"]

    if module.params.get("metadata") is not None:
        payload["metadata"] = module.params["metadata"]

    if module.params.get("model") is not None:
        payload["model"] = module.params["model"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("reasoning_effort") is not None:
        payload["reasoning_effort"] = module.params["reasoning_effort"]

    if module.params.get("response_format") is not None:
        payload["response_format"] = module.params["response_format"]

    if module.params.get("temperature") is not None:
        payload["temperature"] = module.params["temperature"]

    if module.params.get("tool_resources") is not None:
        payload["tool_resources"] = module.params["tool_resources"]

    if module.params.get("tools") is not None:
        payload["tools"] = module.params["tools"]

    if module.params.get("top_p") is not None:
        payload["top_p"] = module.params["top_p"]

    return payload

def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            description=dict(
                type="str",

            ),

            instructions=dict(
                type="str",

            ),

            metadata=dict(
                type="dict",

            ),

            model=dict(
                type="str",

            ),

            name=dict(
                type="str",

            ),

            reasoning_effort=dict(
                type="str",

                choices=['none', 'minimal', 'low', 'medium', 'high', 'xhigh'],

                default="medium",

            ),

            response_format=dict(
                type="str",

                choices=['auto'],

            ),

            temperature=dict(
                type="float",

                default=1,

            ),

            tool_resources=dict(
                type="dict",

            ),

            tools=dict(
                type="list",
                elements="dict",

                default=[],

            ),

            top_p=dict(
                type="float",

                default=1,

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
                        "/assistants/{assistant_id}",
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
                    path = "/assistants/{id}".replace(
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

                result["created_at"] = current.get("created_at")

                result["name"] = current.get("name")

                result["description"] = current.get("description")

                result["model"] = current.get("model")

                result["instructions"] = current.get("instructions")

                result["tools"] = current.get("tools")

                result["tool_resources"] = current.get("tool_resources")

                result["metadata"] = current.get("metadata")

                result["temperature"] = current.get("temperature")

                result["top_p"] = current.get("top_p")

                result["response_format"] = current.get("response_format")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/assistants/{id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

if __name__ == "__main__":
    main()
