#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: response_stream
short_description: Create a streaming response
description:
  - Create a streaming response.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: Model to use.
    type: str
    required: true
  input:
    description: Input text or messages.
    type: raw
    required: true
  stream:
    description: Enable streaming.
    type: bool
    default: true"""

EXAMPLES = r"""
- name: Create a streaming response
  stevefulme1.openai.response_stream:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
response:
  description: The streaming response object.
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
        input=dict(type="raw", required=True),
        stream=dict(type="bool", default=True),
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
        payload = {
            "model": module.params["model"],
            "input": module.params["input"],
            "stream": module.params["stream"],
        }

        resp = client.post("responses", data=payload)
        module.exit_json(changed=True, response=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"response_stream failed: {str(e)}")


if __name__ == "__main__":
    main()
