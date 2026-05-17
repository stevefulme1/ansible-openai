#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: thread_run
short_description: Create a run on an OpenAI thread
description:
  - Executes an assistant on a thread, creating a run.
  - This operation is inherently non-idempotent.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  thread_id:
    description: ID of the thread to run.
    type: str
    required: true
  assistant_id:
    description: ID of the assistant to execute.
    type: str
    required: true
  instructions:
    description: Override instructions for this run.
    type: str
    required: false
  model:
    description: Override the model for this run.
    type: str
    required: false
  metadata:
    description: Metadata key-value pairs.
    type: dict
    required: false
"""

EXAMPLES = r"""
- name: Run an assistant on a thread
  stevefulme1.openai.thread_run:
    api_key: "{{ openai_api_key }}"
    thread_id: thread_abc123
    assistant_id: asst_abc123
  register: result
"""

RETURN = r"""
run:
  description: The run object.
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
        assistant_id=dict(type="str", required=True),
        instructions=dict(type="str", required=False),
        model=dict(type="str", required=False),
        metadata=dict(type="dict", required=False),
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

    payload = dict(assistant_id=module.params["assistant_id"])
    for opt in ("instructions", "model", "metadata"):
        if module.params.get(opt) is not None:
            payload[opt] = module.params[opt]

    try:
        resp = client.post("threads/{}/runs".format(module.params["thread_id"]), data=payload)
        module.exit_json(changed=True, run=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to create run: {str(e)}")


if __name__ == "__main__":
    main()
