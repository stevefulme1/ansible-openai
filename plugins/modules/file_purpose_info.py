#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: file_purpose_info
short_description: List files by purpose
description:
  - List files by purpose.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  purpose:
    description: >-
      Filter files by purpose
      (assistants, fine-tune, batch, vision).
    type: str
    required: true
  limit:
    description:
      - Maximum number of results to return.
    type: int
    default: 100
  offset:
    description:
      - Number of results to skip for pagination.
    type: int
    default: 0
"""

EXAMPLES = r"""
- name: List files by purpose
  stevefulme1.openai.file_purpose_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
files:
  description: List of files filtered by purpose.
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
        purpose=dict(type="str", required=True),
    )
    spec.update(
        limit=dict(type="int", default=100),
        offset=dict(type="int", default=0),
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
        endpoint = "files?purpose={}".format(module.params["purpose"])
        resp = client.get(endpoint)
        module.exit_json(changed=False, files=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"file_purpose_info failed: {str(e)}")


if __name__ == "__main__":
    main()
