#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: chat_completion_with_tools
short_description: Chat completion with function/tool calling
description:
  - Creates a chat completion with tool/function calling support.
  - This operation is inherently non-idempotent.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: ID of the model to use.
    type: str
    required: true
  messages:
    description: List of message objects with role and content.
    type: list
    elements: dict
    required: true
  tools:
    description: List of tool definitions for function calling.
    type: list
    elements: dict
    required: true
  tool_choice:
    description: Controls which tool is called (auto, none, or specific).
    type: raw
    required: false
  temperature:
    description: Sampling temperature between 0 and 2.
    type: float
    required: false
  max_tokens:
    description: Maximum number of tokens to generate.
    type: int
    required: false
"""

EXAMPLES = r"""
- name: Chat with tool calling
  stevefulme1.openai.chat_completion_with_tools:
    api_key: "{{ openai_api_key }}"
    model: gpt-4
    messages:
      - role: user
        content: "What is the weather in Boston?"
    tools:
      - type: function
        function:
          name: get_weather
          description: Get the weather for a location
          parameters:
            type: object
            properties:
              location:
                type: string
            required:
              - location
  register: result
"""

RETURN = r"""
completion:
  description: The chat completion response with tool calls.
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
        model=dict(type="str", required=True),
        messages=dict(type="list", elements="dict", required=True),
        tools=dict(type="list", elements="dict", required=True),
        tool_choice=dict(type="raw", required=False),
        temperature=dict(type="float", required=False),
        max_tokens=dict(type="int", required=False, no_log=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, completion={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    payload = dict(
        model=module.params["model"],
        messages=module.params["messages"],
        tools=module.params["tools"],
    )
    for opt in ("tool_choice", "temperature", "max_tokens"):
        if module.params.get(opt) is not None:
            payload[opt] = module.params[opt]

    try:
        resp = client.post("chat/completions", data=payload)
        module.exit_json(changed=True, completion=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Chat completion with tools failed: {str(e)}")


if __name__ == "__main__":
    main()
