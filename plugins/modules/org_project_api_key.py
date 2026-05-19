#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: org_project_api_key
short_description: Manage per-project API keys
description:
  - Manage per-project API keys.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the API key.
    type: str
    choices: [present, absent]
    default: present
  project_id:
    description: ID of the project.
    type: str
    required: true
  name:
    description: Name for the API key.
    type: str
    required: false
  api_key_id:
    description: ID of existing API key (for delete).
    type: str
    required: false"""

EXAMPLES = r"""
- name: Manage per-project API keys
  stevefulme1.openai.org_project_api_key:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
api_key:
  description: The API key object.
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
        project_id=dict(type="str", required=True),
        name=dict(type="str", required=False),
        api_key_id=dict(type="str", required=False),
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
        pid = module.params["project_id"]
        if module.params["state"] == "absent":
            kid = module.params["api_key_id"]
            resp = client.delete(f"organization/projects/{pid}/api_keys/{kid}")

            # Prevent sensitive values from appearing in logs
            for sensitive_key in ("key", "secret", "token", "api_key"):
                val = resp.get(sensitive_key, "")
                if val:
                    module.no_log_values.add(val)

            module.exit_json(changed=True, api_key=resp)
            return
        payload = {}
        if module.params.get("name"):
            payload["name"] = module.params["name"]

        endpoint = f"organization/projects/{pid}/api_keys"
        resp = client.post(endpoint, data=payload)

        # Prevent sensitive values from appearing in logs
        for sensitive_key in ("key", "secret", "token", "api_key"):
            val = resp.get(sensitive_key, "")
            if val:
                module.no_log_values.add(val)

        module.exit_json(changed=True, api_key=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"org_project_api_key failed: {str(e)}")


if __name__ == "__main__":
    main()
