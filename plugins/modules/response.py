#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: response
short_description: Create a response via the Responses API
description:
  - Create a response via the Responses API.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: Model to use for the response.
    type: str
    required: true
  input:
    description: Input text or messages for the response.
    type: raw
    required: true
  instructions:
    description: System instructions.
    type: str
    required: false
  max_output_tokens:
    description: Maximum output tokens.
    type: int
    required: false
  temperature:
    description: Sampling temperature.
    type: float
    required: false"""

EXAMPLES = r"""
- name: Create a response via the Responses API
  stevefulme1.openai.response:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
response:
  description: The response object.
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
        instructions=dict(type="str", required=False),
        max_output_tokens=dict(type="int", required=False, no_log=False),
        temperature=dict(type="float", required=False),
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
        }
        for opt in ("instructions", "max_output_tokens", "temperature"):
            if module.params.get(opt) is not None:
                payload[opt] = module.params[opt]

        resp = client.post("responses", data=payload)
        module.exit_json(changed=True, response=resp)
    except OpenAIError as e:
        module.fail_json(msg="response failed: %s" % str(e))


if __name__ == "__main__":
    main()
