#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: usage_alert
short_description: Configure usage threshold alerts
description:
  - Configure usage threshold alerts.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  threshold_amount:
    description: Dollar amount threshold for alerts.
    type: float
    required: true
  notification_emails:
    description: Email addresses for notifications.
    type: list
    elements: str
    required: false
  project_id:
    description: Scope alert to a specific project.
    type: str
    required: false"""

EXAMPLES = r"""
- name: Configure usage threshold alerts
  stevefulme1.openai.usage_alert:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
alert:
  description: The usage alert configuration.
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
        threshold_amount=dict(type="float", required=True),
        notification_emails=dict(type="list", elements="str", required=False),
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
        payload = {
            "threshold_amount": (module.params["threshold_amount"]),
        }
        if module.params.get("notification_emails"):
            payload["notification_emails"] = module.params["notification_emails"]
        if module.params.get("project_id"):
            payload["project_id"] = module.params["project_id"]

        resp = client.post("organization/alerts/usage", data=payload)
        module.exit_json(changed=True, alert=resp)
    except OpenAIError as e:
        module.fail_json(msg="usage_alert failed: %s" % str(e))


if __name__ == "__main__":
    main()
