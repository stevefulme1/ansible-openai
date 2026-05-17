#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: org_invite
short_description: Send or manage OpenAI organization invites
description:
  - Sends invitations to join the OpenAI organization or lists pending invites.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the invite.
    type: str
    choices: [present, absent]
    default: present
  email:
    description: Email address to invite.
    type: str
    required: false
  invite_id:
    description: ID of the invite (required for delete).
    type: str
    required: false
  role:
    description: Role for the invited user.
    type: str
    choices: [owner, reader]
    required: false
    default: reader
"""

EXAMPLES = r"""
- name: Send an organization invite
  stevefulme1.openai.org_invite:
    api_key: "{{ openai_api_key }}"
    email: user@example.com
    role: reader

- name: Delete an invite
  stevefulme1.openai.org_invite:
    api_key: "{{ openai_api_key }}"
    invite_id: invite-abc123
    state: absent
"""

RETURN = r"""
invite:
  description: The invite object.
  type: dict
  returned: when state is present
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
        email=dict(type="str", required=False),
        invite_id=dict(type="str", required=False),
        role=dict(type="str", required=False, default="reader", choices=["owner", "reader"]),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ["email"]),
            ("state", "absent", ["invite_id"]),
        ],
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
        if module.params["state"] == "absent":
            client.delete("organization/invites/{}".format(module.params["invite_id"]))
            module.exit_json(changed=True)
        else:
            resp = client.post(
                "organization/invites",
                data={
                    "email": module.params["email"],
                    "role": module.params["role"],
                },
            )
            module.exit_json(changed=True, invite=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Invite operation failed: {str(e)}")


if __name__ == "__main__":
    main()
