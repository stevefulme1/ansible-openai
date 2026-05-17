#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: mcp_tool_policy
short_description: Define which tools AI agents can access
description:
  - Define which tools AI agents can access.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  policy_name:
    description: Name of the tool policy.
    type: str
    required: true
  allowed_tools:
    description: List of allowed tool names.
    type: list
    elements: str
    required: false
  blocked_tools:
    description: List of blocked tool names.
    type: list
    elements: str
    required: false
  project_id:
    description: Scope policy to a project.
    type: str
    required: false"""

EXAMPLES = r"""
- name: Define which tools AI agents can access
  stevefulme1.openai.mcp_tool_policy:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
policy:
  description: The MCP tool policy.
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
        policy_name=dict(type="str", required=True),
        allowed_tools=dict(type="list", elements="str", required=False),
        blocked_tools=dict(type="list", elements="str", required=False),
        project_id=dict(type="str", required=False),
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
        if module.params.get("allowed_tools"):
            payload["allowed_tools"] = module.params["allowed_tools"]
        if module.params.get("blocked_tools"):
            payload["blocked_tools"] = module.params["blocked_tools"]
        if module.params.get("project_id"):
            payload["project_id"] = module.params["project_id"]

        resp = client.post("organization/mcp/policies", data=payload)
        module.exit_json(changed=True, policy=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"mcp_tool_policy failed: {str(e)}")


if __name__ == "__main__":
    main()
