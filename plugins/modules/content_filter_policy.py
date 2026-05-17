#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: content_filter_policy
short_description: Manage content filter policies
description:
  - Manage content filter policies.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the policy.
    type: str
    choices: [present, absent]
    default: present
  policy_name:
    description: Name of the content filter policy.
    type: str
    required: true
  rules:
    description: List of filter rules.
    type: list
    elements: dict
    required: false"""

EXAMPLES = r"""
- name: Manage content filter policies
  stevefulme1.openai.content_filter_policy:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
policy:
  description: Content filter policy.
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
        state=dict(type="str", choices=["present", "absent"], default="present"),
        policy_name=dict(type="str", required=True),
        rules=dict(type="list", elements="dict", required=False),
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
        payload = {"name": module.params["policy_name"]}
        if module.params.get("rules"):
            payload["rules"] = module.params["rules"]

        resp = client.post("moderations", data=payload)
        module.exit_json(changed=True, policy=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"content_filter_policy failed: {str(e)}")


if __name__ == "__main__":
    main()
