#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: file_info
short_description: List files in the OpenAI account
description:
  - Retrieves a list of files uploaded to the OpenAI platform.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  purpose:
    description: Filter files by purpose.
    type: str
    required: false
"""

EXAMPLES = r"""
- name: List all files
  stevefulme1.openai.file_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
files:
  description: List of file objects.
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
    spec["purpose"] = dict(type="str", required=False)

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

    params = {}
    if module.params.get("purpose"):
        params["purpose"] = module.params["purpose"]

    try:
        resp = client.get("files", params=params)
        module.exit_json(changed=False, files=resp.get("data", []))
    except OpenAIError as e:
        module.fail_json(msg="Failed to list files: %s" % str(e))


if __name__ == "__main__":
    main()
