#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: org_billing_info
short_description: Get organization billing details
description:
  - Get organization billing details.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
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
- name: Get organization billing details
  stevefulme1.openai.org_billing_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
billing:
  description: Billing details.
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
    argument_spec = openai_argument_spec()
    argument_spec.update(
        limit=dict(type="int", default=100),
        offset=dict(type="int", default=0),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=False)

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        resp = client.get("organization/billing")
        module.exit_json(changed=False, billing=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"org_billing_info failed: {str(e)}")


if __name__ == "__main__":
    main()
