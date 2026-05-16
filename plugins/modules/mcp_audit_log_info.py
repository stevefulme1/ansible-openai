#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mcp_audit_log_info
short_description: Get MCP action audit trail
description:
  - Get MCP action audit trail.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  start_date:
    description: Start date for audit logs.
    type: str
    required: false
  end_date:
    description: End date for audit logs.
    type: str
    required: false
"""

EXAMPLES = r"""
- name: Get MCP action audit trail
  stevefulme1.openai.mcp_audit_log_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
audit_logs:
  description: List of MCP audit log entries.
  type: list
  returned: always
  elements: dict"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.openai.plugins.module_utils.openai_client import (
    OpenAIClient,
    OpenAIError,
    openai_argument_spec,
)


def main():
    spec = openai_argument_spec()
    spec.update(
        start_date=dict(type="str", required=False),
        end_date=dict(type="str", required=False),
    )
    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=False)

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        params = ""
        if module.params.get("start_date"):
            params += "?start_date=%s" % (module.params["start_date"])
        if module.params.get("end_date"):
            sep = "&" if params else "?"
            params += "%send_date=%s" % (sep, module.params["end_date"])
        endpoint = "organization/mcp/audit_logs" + params
        resp = client.get(endpoint)
        module.exit_json(changed=False, audit_logs=resp)
    except OpenAIError as e:
        module.fail_json(msg="mcp_audit_log_info failed: %s" % str(e))


if __name__ == "__main__":
    main()
