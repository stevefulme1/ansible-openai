#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: org_usage_info
short_description: Get OpenAI organization usage data
description:
  - Retrieves usage data for the organization over a date range.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  start_date:
    description: Start date for usage data (YYYY-MM-DD).
    type: str
    required: true
  end_date:
    description: End date for usage data (YYYY-MM-DD).
    type: str
    required: false
  limit:
    description:
      - Maximum number of results to return.
    type: int
    default: 100
  offset:
    description:
      - Number of results to skip for pagination.
    type: int
    default: 0
"""

EXAMPLES = r"""
- name: Get usage data
  stevefulme1.openai.org_usage_info:
    api_key: "{{ openai_api_key }}"
    start_date: "2024-01-01"
  register: result
"""

RETURN = r"""
usage:
  description: Usage data for the organization.
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
        start_date=dict(type="str", required=True),
        end_date=dict(type="str", required=False),
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

    params = {"start_date": module.params["start_date"]}
    if module.params.get("end_date"):
        params["end_date"] = module.params["end_date"]

    try:
        resp = client.get("organization/usage", params=params)
        module.exit_json(changed=False, usage=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to get usage data: {str(e)}")


if __name__ == "__main__":
    main()
