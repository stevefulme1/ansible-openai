#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: org_audit_log_info
short_description: Get OpenAI organization audit logs
description:
  - Retrieves audit log entries for the organization.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  limit:
    description: Maximum number of audit log entries to return.
    type: int
    required: false
    default: 20
  effective_at_gte:
    description: Filter logs after this timestamp (Unix epoch).
    type: int
    required: false
  effective_at_lte:
    description: Filter logs before this timestamp (Unix epoch).
    type: int
    required: false
  event_types:
    description: Filter by event types.
    type: list
    elements: str
    required: false
"""

EXAMPLES = r"""
- name: Get audit logs
  stevefulme1.openai.org_audit_log_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
audit_logs:
  description: List of audit log entries.
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
        effective_at_gte=dict(type="int", required=False),
        effective_at_lte=dict(type="int", required=False),
        event_types=dict(type="list", elements="str", required=False),
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
    if module.params.get("effective_at_gte"):
        params["effective_at.gte"] = module.params["effective_at_gte"]
    if module.params.get("effective_at_lte"):
        params["effective_at.lte"] = module.params["effective_at_lte"]
    if module.params.get("event_types"):
        params["event_types[]"] = module.params["event_types"]

    try:
        data = client.list_paginated("organization/audit_logs", params=params)
        module.exit_json(changed=False, audit_logs=data)
    except OpenAIError as e:
        module.fail_json(msg="Failed to get audit logs: %s" % str(e))


if __name__ == "__main__":
    main()
