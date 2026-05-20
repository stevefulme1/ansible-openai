#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: assistant
short_description: Create, update, or delete an OpenAI assistant
description:
  - Manages OpenAI assistants lifecycle.
  - Supports create, update, and delete operations.
  - Idempotent -- a second run with identical parameters returns changed=False.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the assistant.
    type: str
    choices: [present, absent]
    default: present
  assistant_id:
    description: ID of an existing assistant (required for update/delete).
    type: str
    required: false
  name:
    description: Name of the assistant. Used for lookup when assistant_id is not provided.
    type: str
    required: false
  model:
    description: Model ID for the assistant.
    type: str
    required: false
  instructions:
    description: System instructions for the assistant.
    type: str
    required: false
  tools:
    description: List of tools enabled for the assistant.
    type: list
    elements: dict
    required: false
  metadata:
    description: Metadata key-value pairs.
    type: dict
    required: false
"""

EXAMPLES = r"""
- name: Create an assistant
  stevefulme1.openai.assistant:
    api_key: "{{ openai_api_key }}"
    model: gpt-4
    name: "My Assistant"
    instructions: "You are a helpful assistant."
  register: result

- name: Update an assistant
  stevefulme1.openai.assistant:
    api_key: "{{ openai_api_key }}"
    assistant_id: asst_abc123
    instructions: "Updated instructions."

- name: Delete an assistant
  stevefulme1.openai.assistant:
    api_key: "{{ openai_api_key }}"
    assistant_id: asst_abc123
    state: absent
"""

RETURN = r"""
assistant:
  description: The assistant object.
  type: dict
  returned: when state is present
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.openai.plugins.module_utils.openai_client import (
    OpenAIClient,
    OpenAIError,
    openai_argument_spec,
)

COMPARE_KEYS = ("model", "name", "instructions", "tools", "metadata")


def get_current_state(client, module):
    """GET the assistant, return None if not found."""
    assistant_id = module.params.get("assistant_id")
    if assistant_id:
        try:
            return client.get("assistants/{0}".format(assistant_id))
        except OpenAIError as e:
            if e.status_code == 404:
                return None
            raise
    name = module.params.get("name")
    if name:
        assistants = client.list_paginated("assistants")
        for a in assistants:
            if a.get("name") == name:
                return a
    return None


def needs_update(current, desired):
    """Compare current state with desired parameters, return dict of changes."""
    changes = {}
    for key in COMPARE_KEYS:
        if desired.get(key) is not None:
            if current.get(key) != desired[key]:
                changes[key] = desired[key]
    return changes


def build_desired(module):
    """Build desired-state dict from module params."""
    desired = {}
    for key in COMPARE_KEYS:
        if module.params.get(key) is not None:
            desired[key] = module.params[key]
    return desired


def main():
    spec = openai_argument_spec()
    spec.update(
        state=dict(type="str", choices=["present", "absent"], default="present"),
        assistant_id=dict(type="str", required=False),
        model=dict(type="str", required=False),
        name=dict(type="str", required=False),
        instructions=dict(type="str", required=False),
        tools=dict(type="list", elements="dict", required=False),
        metadata=dict(type="dict", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("assistant_id", "name"), True),
        ],
    )

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    state = module.params["state"]

    try:
        current = get_current_state(client, module)

        if state == "absent":
            if current is None:
                module.exit_json(changed=False)
            if module.check_mode:
                module.exit_json(changed=True)
            client.delete("assistants/{0}".format(current["id"]))
            module.exit_json(changed=True)
        else:
            desired = build_desired(module)
            if current:
                changes = needs_update(current, desired)
                if not changes:
                    module.exit_json(changed=False, assistant=current)
                if module.check_mode:
                    module.exit_json(changed=True, assistant=current,
                                    diff=dict(before=current, after=changes))
                resp = client.post("assistants/{0}".format(current["id"]), data=changes)
                module.exit_json(changed=True, assistant=resp)
            else:
                if module.check_mode:
                    module.exit_json(changed=True, assistant={})
                resp = client.post("assistants", data=desired)
                module.exit_json(changed=True, assistant=resp)
    except OpenAIError as e:
        module.fail_json(msg="Assistant operation failed: {0}".format(str(e)))


if __name__ == "__main__":
    main()
