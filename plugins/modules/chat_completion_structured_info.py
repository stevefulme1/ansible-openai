#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: chat_completion_structured_info
short_description: Get details of a structured OpenAI chat completion
description:
  - Retrieves information about OpenAI completion.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  completion_id:
    description: ID of a specific completion to retrieve.
    type: str
    required: false
  limit:
    description: Maximum number of results to return.
    type: int
    required: false
    default: 100
"""

EXAMPLES = r"""
- name: Get details of a structured OpenAI chat completion
  stevefulme1.openai.chat_completion_structured_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
completion:
  description: The completion data.
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
    spec["completion_id"] = dict(type="str", required=False)
    spec["limit"] = dict(type="int", required=False, default=100)

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
        if module.params.get("id"):
            resp = client.get("chat/completions/{completion_id}".format(completion_id=module.params["completion_id"]))
            module.exit_json(changed=False, completion=resp)
        else:
            data = client.list_paginated("chat/completions", params={"limit": module.params["limit"]})
            module.exit_json(changed=False, completion=data)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to retrieve completion: {str(e)}")


if __name__ == "__main__":
    main()
