#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: org_api_key
short_description: Manage OpenAI API keys
description:
  - Deletes API keys in the organization. Keys are created via the dashboard.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  key_id:
    description: ID of the API key to delete.
    type: str
    required: true
  state:
    description: Desired state of the API key.
    type: str
    choices: [absent]
    default: absent
"""

EXAMPLES = r"""
- name: Delete an API key
  stevefulme1.openai.org_api_key:
    api_key: "{{ openai_api_key }}"
    key_id: key-abc123
    state: absent
"""

RETURN = r"""
deleted:
  description: Whether the key was deleted.
  type: bool
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
        key_id=dict(type="str", required=True),
        state=dict(type="str", choices=["absent"], default="absent"),
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
        client.delete("organization/api_keys/{}".format(module.params["key_id"]))
        module.exit_json(changed=True, deleted=True)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to delete API key: {str(e)}")


if __name__ == "__main__":
    main()
