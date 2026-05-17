#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: thread_run_cancel
short_description: Cancel an OpenAI thread run
description:
  - Cancels an in-progress run on a thread.
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
    description: ID of the run to cancel.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Cancel a run
  stevefulme1.openai.thread_run_cancel:
    api_key: "{{ openai_api_key }}"
    thread_id: thread_abc123
    run_id: run_abc123
"""

RETURN = r"""
run:
  description: The cancelled run object.
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

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, run={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        resp = client.post("threads/{}/runs/{}/cancel".format(module.params["thread_id"], module.params["run_id"]))
        module.exit_json(changed=True, run=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to cancel run: {str(e)}")


if __name__ == "__main__":
    main()
