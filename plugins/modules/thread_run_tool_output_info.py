#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: thread_run_tool_output_info
short_description: Get tool output status of an OpenAI thread run
description:
  - Retrieves information about OpenAI run.
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
"""

EXAMPLES = r"""
- name: Get tool output status of an OpenAI thread run
  stevefulme1.openai.thread_run_tool_output_info:
    api_key: "{{ openai_api_key }}"
    thread_id: "example_thread_id"
    run_id: "example_run_id"
  register: result
"""

RETURN = r"""
run:
  description: The run data.
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
    spec["thread_id"] = dict(type="str", required=True)
    spec["run_id"] = dict(type="str", required=True)

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
        resp = client.get(
            "threads/{thread_id}/runs/{run_id}".format(
                thread_id=module.params["thread_id"], run_id=module.params["run_id"]
            )
        )
        module.exit_json(changed=False, run=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to retrieve run: {str(e)}")


if __name__ == "__main__":
    main()
