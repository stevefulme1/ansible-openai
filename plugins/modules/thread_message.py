#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: thread_message
short_description: Create a message in an OpenAI thread
description:
  - Adds a message to an existing assistant thread.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  thread_id:
    description: ID of the thread to add the message to.
    type: str
    required: true
  role:
    description: Role of the message sender.
    type: str
    choices: [user, assistant]
    default: user
  content:
    description: Content of the message.
    type: str
    required: true
  metadata:
    description: Metadata key-value pairs.
    type: dict
    required: false
"""

EXAMPLES = r"""
- name: Add a message to a thread
  stevefulme1.openai.thread_message:
    api_key: "{{ openai_api_key }}"
    thread_id: thread_abc123
    content: "Hello, can you help me?"
  register: result
"""

RETURN = r"""
message:
  description: The created message object.
  type: dict
  returned: always
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
        thread_id=dict(type="str", required=True),
        role=dict(type="str", choices=["user", "assistant"], default="user"),
        content=dict(type="str", required=True),
        metadata=dict(type="dict", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, message={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    payload = dict(
        role=module.params["role"],
        content=module.params["content"],
    )
    if module.params.get("metadata"):
        payload["metadata"] = module.params["metadata"]

    try:
        resp = client.post("threads/{}/messages".format(module.params["thread_id"]), data=payload)
        module.exit_json(changed=True, message=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to create message: {str(e)}")


if __name__ == "__main__":
    main()
