#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: assistant_tool
short_description: Manage assistant tools
description:
  - Manage assistant tools.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  assistant_id:
    description: ID of the assistant.
    type: str
    required: true
  tools:
    description: >-
      List of tools (code_interpreter, file_search, function).
    type: list
    elements: dict
    required: true"""

EXAMPLES = r"""
- name: Manage assistant tools
  stevefulme1.openai.assistant_tool:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
assistant:
  description: The updated assistant object.
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
        assistant_id=dict(type="str", required=True),
        tools=dict(type="list", elements="dict", required=True),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
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
        payload = {"tools": module.params["tools"]}

        endpoint = "assistants/{}".format(module.params["assistant_id"])
        resp = client.post(endpoint, data=payload)
        module.exit_json(changed=True, assistant=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"assistant_tool failed: {str(e)}")


if __name__ == "__main__":
    main()
