#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: assistant
short_description: Create, update, or delete an OpenAI assistant
description:
  - Manages OpenAI assistants lifecycle.
  - Supports create, update, and delete operations.
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
  model:
    description: Model ID for the assistant.
    type: str
    required: false
  name:
    description: Name of the assistant.
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
  file_ids:
    description: List of file IDs attached to the assistant.
    type: list
    elements: str
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


def main():
    spec = openai_argument_spec()
    spec.update(
        state=dict(type="str", choices=["present", "absent"], default="present"),
        assistant_id=dict(type="str", required=False),
        model=dict(type="str", required=False),
        name=dict(type="str", required=False),
        instructions=dict(type="str", required=False),
        tools=dict(type="list", elements="dict", required=False),
        file_ids=dict(type="list", elements="str", required=False),
        metadata=dict(type="dict", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ["assistant_id"]),
        ],
    )

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    state = module.params["state"]
    assistant_id = module.params.get("assistant_id")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        if state == "absent":
            client.delete(f"assistants/{assistant_id}")
            module.exit_json(changed=True)
        else:
            payload = {}
            for opt in (
                "model",
                "name",
                "instructions",
                "tools",
                "file_ids",
                "metadata",
            ):
                if module.params.get(opt) is not None:
                    payload[opt] = module.params[opt]

            if assistant_id:
                resp = client.post(f"assistants/{assistant_id}", data=payload)
            else:
                resp = client.post("assistants", data=payload)
            module.exit_json(changed=True, assistant=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Assistant operation failed: {str(e)}")


if __name__ == "__main__":
    main()
