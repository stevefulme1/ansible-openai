#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: thread_run_tool_output
short_description: Submit tool outputs for a run
description:
  - Submit tool outputs for a run.
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
  tool_outputs:
    description: List of tool output objects.
    type: list
    elements: dict
    required: true"""

EXAMPLES = r"""
- name: Submit tool outputs for a run
  stevefulme1.openai.thread_run_tool_output:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
run:
  description: The updated run object.
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
        thread_id=dict(type="str", required=True),
        run_id=dict(type="str", required=True),
        tool_outputs=dict(type="list", elements="dict", required=True),
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
        payload = {"tool_outputs": module.params["tool_outputs"]}

        tid = module.params["thread_id"]
        rid = module.params["run_id"]
        endpoint = f"threads/{tid}/runs/{rid}/submit_tool_outputs"
        resp = client.post(endpoint, data=payload)
        module.exit_json(changed=True, run=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"thread_run_tool_output failed: {str(e)}")


if __name__ == "__main__":
    main()
