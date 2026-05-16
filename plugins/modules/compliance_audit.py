#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: compliance_audit
short_description: Generate compliance audit reports
description:
  - Generate compliance audit reports.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  start_date:
    description: Audit start date (YYYY-MM-DD).
    type: str
    required: true
  end_date:
    description: Audit end date (YYYY-MM-DD).
    type: str
    required: true
  event_types:
    description: Filter by event types.
    type: list
    elements: str
    required: false
"""

EXAMPLES = r"""
- name: Generate compliance audit reports
  stevefulme1.openai.compliance_audit:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
audit_report:
  description: Compliance audit report.
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
        start_date=dict(type="str", required=True),
        end_date=dict(type="str", required=True),
        event_types=dict(type="list", elements="str", required=False),
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
        params = "?start_date=%s&end_date=%s" % (
            module.params["start_date"],
            module.params["end_date"],
        )
        if module.params.get("event_types"):
            for et in module.params["event_types"]:
                params += "&event_types[]=%s" % et
        endpoint = "organization/audit_logs" + params
        resp = client.get(endpoint)
        module.exit_json(changed=False, audit_report=resp)
    except OpenAIError as e:
        module.fail_json(msg="compliance_audit failed: %s" % str(e))


if __name__ == "__main__":
    main()
