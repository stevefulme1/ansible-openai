#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: org_project_member
short_description: Manage project membership
description:
  - Manage project membership.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of membership.
    type: str
    choices: [present, absent]
    default: present
  project_id:
    description: ID of the project.
    type: str
    required: true
  user_id:
    description: ID of the user.
    type: str
    required: true
  role:
    description: Role for the member.
    type: str
    choices: [member, owner]
    default: member"""

EXAMPLES = r"""
- name: Manage project membership
  stevefulme1.openai.org_project_member:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
member:
  description: The project member object.
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
        user_id=dict(type="str", required=True),
        role=dict(type="str", choices=["member", "owner"], default="member"),
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
        uid = module.params["user_id"]
        if module.params["state"] == "absent":
            resp = client.delete(f"organization/projects/{pid}/users/{uid}")
            module.exit_json(changed=True, member=resp)
            return
        payload = {
            "user_id": uid,
            "role": module.params["role"],
        }

        endpoint = f"organization/projects/{pid}/users"
        resp = client.post(endpoint, data=payload)
        module.exit_json(changed=True, member=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"org_project_member failed: {str(e)}")


if __name__ == "__main__":
    main()
