#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: thread_run_info
short_description: Get OpenAI thread run status and details
description:
  - Retrieves details and status of a run on a thread.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  thread_id:
    description: ID of the thread.
    type: str
    required: true
  run_id:
    description: ID of the run to retrieve.
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
- name: Get run status
  stevefulme1.openai.thread_run_info:
    api_key: "{{ openai_api_key }}"
    thread_id: thread_abc123
    run_id: run_abc123
  register: result
"""

RETURN = r"""
run:
  description: The run object with status details.
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
    )
    spec.update(
        limit=dict(type="int", default=100),
        offset=dict(type="int", default=0),
    )

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
        resp = client.get("threads/{}/runs/{}".format(module.params["thread_id"], module.params["run_id"]))
        module.exit_json(changed=False, run=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to get run: {str(e)}")


if __name__ == "__main__":
    main()
