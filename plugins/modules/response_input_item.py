#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: response_input_item
short_description: Manage response input items
description:
  - Manage response input items.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  response_id:
    description: ID of the response.
    type: str
    required: true
  items:
    description: List of input items.
    type: list
    elements: dict
    required: true"""

EXAMPLES = r"""
- name: Manage response input items
  stevefulme1.openai.response_input_item:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
input_item:
  description: The input item object.
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
        response_id=dict(type="str", required=True),
        items=dict(type="list", elements="dict", required=True),
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
        payload = {"input": module.params["items"]}

        endpoint = "responses/{}/input_items".format(module.params["response_id"])
        resp = client.post(endpoint, data=payload)
        module.exit_json(changed=True, input_item=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"response_input_item failed: {str(e)}")


if __name__ == "__main__":
    main()
