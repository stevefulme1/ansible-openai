#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: response_stream_info
short_description: Get details of an OpenAI streaming response
description:
  - Retrieves information about OpenAI response.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  response_id:
    description: ID of the response.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Get details of an OpenAI streaming response
  stevefulme1.openai.response_stream_info:
    api_key: "{{ openai_api_key }}"
    response_id: "example_response_id"
  register: result
"""

RETURN = r"""
response:
  description: The response data.
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
    spec["response_id"] = dict(type="str", required=True)

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
        resp = client.get("responses/{response_id}".format(response_id=module.params["response_id"]))
        module.exit_json(changed=False, response=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to retrieve response: {str(e)}")


if __name__ == "__main__":
    main()
