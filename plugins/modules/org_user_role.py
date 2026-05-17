#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: org_user_role
short_description: Manage OpenAI organization user roles
description:
  - Updates the role of a user in the organization.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  user_id:
    description: ID of the user to update.
    type: str
    required: true
  role:
    description: The role to assign to the user.
    type: str
    choices: [owner, reader]
    required: true
"""

EXAMPLES = r"""
- name: Set user role to reader
  stevefulme1.openai.org_user_role:
    api_key: "{{ openai_api_key }}"
    user_id: user-abc123
    role: reader
"""

RETURN = r"""
user:
  description: The updated user object.
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
        user_id=dict(type="str", required=True),
        role=dict(type="str", required=True, choices=["owner", "reader"]),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, user={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        resp = client.post(
            "organization/users/{}".format(module.params["user_id"]),
            data={"role": module.params["role"]},
        )
        module.exit_json(changed=True, user=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to update user role: {str(e)}")


if __name__ == "__main__":
    main()
