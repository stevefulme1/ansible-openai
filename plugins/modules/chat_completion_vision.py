#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: chat_completion_vision
short_description: Chat completion with image inputs
description:
  - Creates a chat completion that can process image inputs.
  - This operation is inherently non-idempotent.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: ID of the model to use (must support vision).
    type: str
    required: true
  messages:
    description: List of message objects, content may include image URLs.
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
"""

EXAMPLES = r"""
- name: Analyze an image
  stevefulme1.openai.chat_completion_vision:
    api_key: "{{ openai_api_key }}"
    model: gpt-4o
    messages:
      - role: user
        content:
          - type: text
            text: "What is in this image?"
          - type: image_url
            image_url:
              url: "https://example.com/image.png"
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
    )
    for opt in ("temperature", "max_tokens"):
        if module.params.get(opt) is not None:
            payload[opt] = module.params[opt]

    try:
        resp = client.post("chat/completions", data=payload)
        module.exit_json(changed=True, completion=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Vision chat completion failed: {str(e)}")


if __name__ == "__main__":
    main()
