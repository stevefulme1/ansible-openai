#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: thread
short_description: Manage assistants
version_added: "1.0.0"
description:
  - Create, update, and delete thread resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the thread resource.
    type: str
    choices: ['present', 'absent']
    default: present

  messages:
    description:
      - >-
        A list of messages(/docs/api-reference/messages) to start the thread with.
    type: list
    elements: dict

  metadata:
    description:
      - >-
        Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
    type: dict

  tool_resources:
    description:
      - >-
        A set of resources that are made available to the assistant's tools in this thread. The...
    type: dict

extends_documentation_fragment:
  - stevefulme1.openai.auth
"""

EXAMPLES = r"""

- name: Create a thread
  stevefulme1.openai.thread:

    state: present
  # API: POST /threads/{thread_id}

- name: Update a thread
  stevefulme1.openai.thread:
    id: "existing_id"

    messages: "updated_messages"

    metadata: "updated_metadata"

    tool_resources: "updated_tool_resources"

    state: present
  # API:

- name: Delete a thread
  stevefulme1.openai.thread:
    id: "existing_id"
    state: absent
  # API: DELETE /threads/{thread_id}

"""

RETURN = r"""

id:
  description: >-
    The identifier, which can be referenced in API endpoints.
  returned: success
  type: str

object:
  description: >-
    The object type, which is always thread.
  returned: success
  type: str

created_at:
  description: >-
    The Unix timestamp (in seconds) for when the thread was created.
  returned: success
  type: int

tool_resources:
  description: >-
    A set of resources that are made available to the assistant's tools in this thread. The...
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
    """Retrieve the current state of the thread via GET."""

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

    if module.params.get("messages") is not None:
        payload["messages"] = module.params["messages"]

    if module.params.get("metadata") is not None:
        payload["metadata"] = module.params["metadata"]

    if module.params.get("tool_resources") is not None:
        payload["tool_resources"] = module.params["tool_resources"]

    return payload

def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            messages=dict(
                type="list",
                elements="dict",

            ),

            metadata=dict(
                type="dict",

            ),

            tool_resources=dict(
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
                        "/threads/{thread_id}",
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
                    path = "/threads/{id}".replace(
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

                result["tool_resources"] = current.get("tool_resources")

                result["metadata"] = current.get("metadata")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/threads/{id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

if __name__ == "__main__":
    main()
