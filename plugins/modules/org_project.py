#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: org_project
short_description: Manage OpenAI organization projects
description:
  - Creates, updates, or archives projects in the organization.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the project.
    type: str
    choices: [present, archived]
    default: present
  project_id:
    description: ID of the project (required for update/archive).
    type: str
    required: false
  name:
    description: Name of the project.
    type: str
    required: false
"""

EXAMPLES = r"""
- name: Create a project
  stevefulme1.openai.org_project:
    api_key: "{{ openai_api_key }}"
    name: "Production AI"
  register: result

- name: Archive a project
  stevefulme1.openai.org_project:
    api_key: "{{ openai_api_key }}"
    project_id: proj_abc123
    state: archived
"""

RETURN = r"""
project:
  description: The project object.
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
        state=dict(type="str", choices=["present", "archived"], default="present"),
        project_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_if=[("state", "archived", ["project_id"])],
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
        if module.params["state"] == "archived":
            resp = client.post("organization/projects/{}/archive".format(module.params["project_id"]))
            module.exit_json(changed=True, project=resp)
        elif module.params.get("project_id"):
            payload = {}
            if module.params.get("name"):
                payload["name"] = module.params["name"]
            resp = client.post(
                "organization/projects/{}".format(module.params["project_id"]),
                data=payload,
            )
            module.exit_json(changed=True, project=resp)
        else:
            resp = client.post(
                "organization/projects",
                data={"name": module.params["name"]},
            )
            module.exit_json(changed=True, project=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Project operation failed: {str(e)}")


if __name__ == "__main__":
    main()
