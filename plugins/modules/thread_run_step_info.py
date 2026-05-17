#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: thread_run_step_info
short_description: Get run step details
description:
  - Get run step details.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  thread_id:
    description: ID of the thread.
    type: str
    required: true
  run_id:
    description: ID of the run.
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
- name: Get run step details
  stevefulme1.openai.thread_run_step_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
steps:
  description: Run step details.
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
        thread_id=dict(type="str", required=True),
        run_id=dict(type="str", required=True),
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
        tid = module.params["thread_id"]
        rid = module.params["run_id"]
        endpoint = f"threads/{tid}/runs/{rid}/steps"
        resp = client.get(endpoint)
        module.exit_json(changed=False, steps=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"thread_run_step_info failed: {str(e)}")


if __name__ == "__main__":
    main()
