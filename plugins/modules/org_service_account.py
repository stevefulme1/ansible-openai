#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: org_service_account
short_description: Manage organization service accounts
description:
  - Manage organization service accounts.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state.
    type: str
    choices: [present, absent]
    default: present
  project_id:
    description: ID of the project.
    type: str
    required: true
  name:
    description: Name for the service account.
    type: str
    required: false
  service_account_id:
    description: >-
      ID of existing service account (for delete).
    type: str
    required: false"""

EXAMPLES = r"""
- name: Manage organization service accounts
  stevefulme1.openai.org_service_account:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
service_account:
  description: The service account object.
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
        state=dict(type="str", choices=["present", "absent"], default="present"),
        project_id=dict(type="str", required=True),
        name=dict(type="str", required=False),
        service_account_id=dict(type="str", required=False),
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
        pid = module.params["project_id"]
        if module.params["state"] == "absent":
            sid = module.params["service_account_id"]
            resp = client.delete(
                "organization/projects/%s/service_accounts/%s" % (pid, sid)
            )
            module.exit_json(changed=True, service_account=resp)
            return
        payload = {}
        if module.params.get("name"):
            payload["name"] = module.params["name"]

        endpoint = "organization/projects/%s/service_accounts" % pid
        resp = client.post(endpoint, data=payload)
        module.exit_json(changed=True, service_account=resp)
    except OpenAIError as e:
        module.fail_json(msg="org_service_account failed: %s" % str(e))


if __name__ == "__main__":
    main()
