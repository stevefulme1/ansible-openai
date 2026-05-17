#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: mcp_server_config
short_description: Configure AAP MCP server connection
description:
  - Configure AAP MCP server connection.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  server_url:
    description: URL of the MCP server.
    type: str
    required: true
  server_name:
    description: Display name for the server.
    type: str
    required: true
  auth_token:
    description: Authentication token for MCP server.
    type: str
    required: false
  capabilities:
    description: List of server capabilities.
    type: list
    elements: str
    required: false"""

EXAMPLES = r"""
- name: Configure AAP MCP server connection
  stevefulme1.openai.mcp_server_config:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
server:
  description: The MCP server configuration.
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
        server_url=dict(type="str", required=True),
        server_name=dict(type="str", required=True),
        auth_token=dict(type="str", required=False, no_log=True),
        capabilities=dict(type="list", elements="str", required=False),
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
            "url": module.params["server_url"],
            "name": module.params["server_name"],
        }
        if module.params.get("auth_token"):
            payload["auth_token"] = module.params["auth_token"]
        if module.params.get("capabilities"):
            payload["capabilities"] = module.params["capabilities"]

        resp = client.post("organization/mcp/servers", data=payload)
        module.exit_json(changed=True, server=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"mcp_server_config failed: {str(e)}")


if __name__ == "__main__":
    main()
