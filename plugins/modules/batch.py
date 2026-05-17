#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: batch
short_description: Create an OpenAI batch job
description:
  - Creates a batch processing job for asynchronous API requests.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  input_file_id:
    description: ID of the JSONL file with batch requests.
    type: str
    required: true
  endpoint:
    description: The API endpoint for batch processing.
    type: str
    required: true
  completion_window:
    description: Time window for batch completion.
    type: str
    required: false
    default: 24h
  metadata:
    description: Metadata key-value pairs.
    type: dict
    required: false
"""

EXAMPLES = r"""
- name: Create a batch job
  stevefulme1.openai.batch:
    api_key: "{{ openai_api_key }}"
    input_file_id: file-abc123
    endpoint: /v1/chat/completions
  register: result
"""

RETURN = r"""
batch:
  description: The batch job object.
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
        input_file_id=dict(type="str", required=True),
        endpoint=dict(type="str", required=True),
        completion_window=dict(type="str", required=False, default="24h"),
        metadata=dict(type="dict", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, batch={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    payload = dict(
        input_file_id=module.params["input_file_id"],
        endpoint=module.params["endpoint"],
        completion_window=module.params["completion_window"],
    )
    if module.params.get("metadata"):
        payload["metadata"] = module.params["metadata"]

    try:
        resp = client.post("batches", data=payload)
        module.exit_json(changed=True, batch=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Batch creation failed: {str(e)}")


if __name__ == "__main__":
    main()
