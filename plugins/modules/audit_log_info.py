#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: audit_log_info
short_description: Get organization audit logs
description:
  - Retrieves audit log entries for the organization.
  - Shows API key usage, user actions, and administrative events.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  effective_at:
    description: Filter logs after this timestamp (Unix epoch or ISO 8601).
    type: str
  event_types:
    description: Filter to specific event types.
    type: list
    elements: str
  actor_ids:
    description: Filter to specific actor user IDs.
    type: list
    elements: str
  limit:
    description: Maximum number of log entries to return.
    type: int
    default: 20
  after:
    description: Cursor for forward pagination.
    type: str
  before:
    description: Cursor for backward pagination.
    type: str
"""

EXAMPLES = r"""
- name: Get recent audit logs
  stevefulme1.openai.audit_log_info:
    api_key: "{{ openai_api_key }}"
  register: result

- name: Get audit logs for specific events
  stevefulme1.openai.audit_log_info:
    api_key: "{{ openai_api_key }}"
    event_types:
      - api_key.created
      - api_key.deleted
    limit: 50
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
        effective_at=dict(type="str"),
        event_types=dict(type="list", elements="str"),
        actor_ids=dict(type="list", elements="str"),
        limit=dict(type="int", default=20),
        after=dict(type="str"),
        before=dict(type="str"),
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
    if module.params.get("effective_at"):
        params["effective_at[gte]"] = module.params["effective_at"]
    if module.params.get("event_types"):
        params["event_types[]"] = module.params["event_types"]
    if module.params.get("actor_ids"):
        params["actor_ids[]"] = module.params["actor_ids"]
    if module.params.get("after"):
        params["after"] = module.params["after"]
    if module.params.get("before"):
        params["before"] = module.params["before"]

    try:
        resp = client.get("organization/audit_logs", params=params)
        module.exit_json(changed=False, audit_logs=resp.get("data", []))
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to get audit logs: {str(e)}")


if __name__ == "__main__":
    main()
