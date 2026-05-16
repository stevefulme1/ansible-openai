#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: governance_dashboard_info
short_description: Get governance metrics dashboard
description:
  - Get governance metrics dashboard.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
"""

EXAMPLES = r"""
- name: Get governance metrics dashboard
  stevefulme1.openai.governance_dashboard_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
dashboard:
  description: Governance dashboard metrics.
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
    module = AnsibleModule(
        argument_spec=openai_argument_spec(),
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
        resp = client.get("organization/usage")
        module.exit_json(changed=False, dashboard=resp)
    except OpenAIError as e:
        module.fail_json(msg="governance_dashboard_info failed: %s" % str(e))


if __name__ == "__main__":
    main()
