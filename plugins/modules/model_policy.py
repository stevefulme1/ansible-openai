#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: model_policy
short_description: Define allowed or blocked models per project
description:
  - Define allowed or blocked models per project.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  project_id:
    description: ID of the project.
    type: str
    required: true
  allowed_models:
    description: List of allowed model IDs.
    type: list
    elements: str
    required: false
  blocked_models:
    description: List of blocked model IDs.
    type: list
    elements: str
    required: false"""

EXAMPLES = r"""
- name: Define allowed or blocked models per project
  stevefulme1.openai.model_policy:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
policy:
  description: The model policy object.
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
        project_id=dict(type="str", required=True),
        allowed_models=dict(type="list", elements="str", required=False),
        blocked_models=dict(type="list", elements="str", required=False),
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
            "project_id": module.params["project_id"],
        }
        if module.params.get("allowed_models"):
            payload["allowed_models"] = module.params["allowed_models"]
        if module.params.get("blocked_models"):
            payload["blocked_models"] = module.params["blocked_models"]

        resp = client.post("organization/policies/models", data=payload)
        module.exit_json(changed=True, policy=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"model_policy failed: {str(e)}")


if __name__ == "__main__":
    main()
