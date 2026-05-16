#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: chat_completion
short_description: Create an OpenAI chat completion
description:
  - Sends messages to a model and returns a chat completion response.
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
  temperature:
    description: Sampling temperature between 0 and 2.
    type: float
    required: false
  max_tokens:
    description: Maximum number of tokens to generate.
    type: int
    required: false
  top_p:
    description: Nucleus sampling parameter.
    type: float
    required: false
  frequency_penalty:
    description: Frequency penalty between -2.0 and 2.0.
    type: float
    required: false
  presence_penalty:
    description: Presence penalty between -2.0 and 2.0.
    type: float
    required: false
  stop:
    description: Sequences where the API will stop generating.
    type: list
    elements: str
    required: false
"""

EXAMPLES = r"""
- name: Create a chat completion
  stevefulme1.openai.chat_completion:
    api_key: "{{ openai_api_key }}"
    model: gpt-4
    messages:
      - role: user
        content: "Hello, world!"
  register: result
"""

RETURN = r"""
completion:
  description: The chat completion response.
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
        temperature=dict(type="float", required=False),
        max_tokens=dict(type="int", required=False),
        top_p=dict(type="float", required=False),
        frequency_penalty=dict(type="float", required=False),
        presence_penalty=dict(type="float", required=False),
        stop=dict(type="list", elements="str", required=False),
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
    )
    for opt in (
        "temperature",
        "max_tokens",
        "top_p",
        "frequency_penalty",
        "presence_penalty",
        "stop",
    ):
        if module.params.get(opt) is not None:
            payload[opt] = module.params[opt]

    try:
        resp = client.post("chat/completions", data=payload)
        module.exit_json(changed=True, completion=resp)
    except OpenAIError as e:
        module.fail_json(msg="Chat completion failed: %s" % str(e))


if __name__ == "__main__":
    main()
