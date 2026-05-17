#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: thread_message_info
short_description: List messages in an OpenAI thread
description:
  - Retrieves messages from an assistant thread.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  thread_id:
    description: ID of the thread to list messages from.
    type: str
    required: true
  limit:
    description: Maximum number of messages to return.
    type: int
    required: false
    default: 100
  offset:
    description: Number of items to skip for pagination.
    type: int
    required: false
    default: 0
"""

EXAMPLES = r"""
- name: List thread messages
  stevefulme1.openai.thread_message_info:
    api_key: "{{ openai_api_key }}"
    thread_id: thread_abc123
  register: result
"""

RETURN = r"""
messages:
  description: List of message objects.
  type: list
  returned: always
  elements: dict
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
        limit=dict(type="int", required=False, default=20),
    )
    spec.update(
        limit=dict(type="int", default=100),
        offset=dict(type="int", default=0),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        data = client.list_paginated(
            "threads/{}/messages".format(module.params["thread_id"]),
            params={"limit": module.params["limit"]},
        )
        module.exit_json(changed=False, messages=data)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to list messages: {str(e)}")


if __name__ == "__main__":
    main()
