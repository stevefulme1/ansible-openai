#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: assistant_info
short_description: List OpenAI assistants
description:
  - Retrieves a list of assistants in the organization.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  limit:
    description: Maximum number of assistants to return.
    type: int
    required: false
    default: 100
  offset:
    description:
      - Number of results to skip for pagination.
    type: int
    default: 0
"""

EXAMPLES = r"""
- name: List assistants
  stevefulme1.openai.assistant_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
assistants:
  description: List of assistant objects.
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
    spec["limit"] = dict(type="int", required=False, default=100)
    spec["offset"] = dict(type="int", required=False, default=0)

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

    try:
        data = client.list_paginated(
            "assistants", params={"limit": module.params["limit"]}
        )
        module.exit_json(changed=False, assistants=data)
    except OpenAIError as e:
        module.fail_json(msg="Failed to list assistants: %s" % str(e))


if __name__ == "__main__":
    main()
