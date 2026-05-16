#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: org_rate_limit_info
short_description: Get OpenAI rate limit status
description:
  - Retrieves current rate limit information for the organization.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
"""

EXAMPLES = r"""
- name: Get rate limit status
  stevefulme1.openai.org_rate_limit_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
rate_limits:
  description: Rate limit information.
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

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        resp = client.get("organization/rate_limits")
        module.exit_json(changed=False, rate_limits=resp)
    except OpenAIError as e:
        module.fail_json(msg="Failed to get rate limits: %s" % str(e))


if __name__ == "__main__":
    main()
