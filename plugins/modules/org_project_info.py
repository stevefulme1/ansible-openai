#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: org_project_info
short_description: List OpenAI organization projects
description:
  - Retrieves a list of projects in the organization.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  limit:
    description: Maximum number of projects to return.
    type: int
    required: false
    default: 100
  offset:
    description: Number of results to skip for pagination.
    type: int
    required: false
    default: 0
  include_archived:
    description: Whether to include archived projects.
    type: bool
    required: false
    default: false
"""

EXAMPLES = r"""
- name: List organization projects
  stevefulme1.openai.org_project_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
projects:
  description: List of project objects.
  type: list
  returned: always
  elements: dict
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
        limit=dict(type="int", required=False, default=20),
        include_archived=dict(type="bool", required=False, default=False),
    )
    spec.update(
        limit=dict(type="int", default=100),
        offset=dict(type="int", default=0),
    )

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

    params = {"limit": module.params["limit"]}
    if module.params["include_archived"]:
        params["include_archived"] = "true"

    try:
        data = client.list_paginated("organization/projects", params=params)
        module.exit_json(changed=False, projects=data)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to list projects: {str(e)}")


if __name__ == "__main__":
    main()
