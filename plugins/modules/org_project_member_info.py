#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: org_project_member_info
short_description: List members of an OpenAI project
description:
  - Retrieves information about OpenAI members.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  project_id:
    description: ID of the project.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: List members of an OpenAI project
  stevefulme1.openai.org_project_member_info:
    api_key: "{{ openai_api_key }}"
    project_id: "example_project_id"
  register: result
"""

RETURN = r"""
members:
  description: The members data.
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
    spec["project_id"] = dict(type="str", required=True)

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
        resp = client.get("organization/projects/{project_id}/users".format(project_id=module.params["project_id"]))
        module.exit_json(changed=False, members=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to retrieve members: {str(e)}")


if __name__ == "__main__":
    main()
