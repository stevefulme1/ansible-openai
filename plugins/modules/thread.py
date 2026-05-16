#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: thread
short_description: Create or delete an OpenAI thread
description:
  - Manages OpenAI assistant threads.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the thread.
    type: str
    choices: [present, absent]
    default: present
  thread_id:
    description: ID of the thread (required for delete).
    type: str
    required: false
  messages:
    description: Initial messages for the thread.
    type: list
    elements: dict
    required: false
  metadata:
    description: Metadata key-value pairs.
    type: dict
    required: false
"""

EXAMPLES = r"""
- name: Create a thread
  stevefulme1.openai.thread:
    api_key: "{{ openai_api_key }}"
  register: result

- name: Delete a thread
  stevefulme1.openai.thread:
    api_key: "{{ openai_api_key }}"
    thread_id: thread_abc123
    state: absent
"""

RETURN = r"""
thread:
  description: The thread object.
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
        thread_id=dict(type="str", required=False),
        messages=dict(type="list", elements="dict", required=False),
        metadata=dict(type="dict", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_if=[("state", "absent", ["thread_id"])],
    )

    if module.check_mode:
        module.exit_json(changed=True)

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        if module.params["state"] == "absent":
            client.delete("threads/%s" % module.params["thread_id"])
            module.exit_json(changed=True)
        else:
            payload = {}
            if module.params.get("messages"):
                payload["messages"] = module.params["messages"]
            if module.params.get("metadata"):
                payload["metadata"] = module.params["metadata"]
            resp = client.post("threads", data=payload)
            module.exit_json(changed=True, thread=resp)
    except OpenAIError as e:
        module.fail_json(msg="Thread operation failed: %s" % str(e))


if __name__ == "__main__":
    main()
