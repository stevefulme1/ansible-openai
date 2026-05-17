#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: vector_store_file_batch
short_description: Batch add files to an OpenAI vector store
description:
  - Adds multiple files to a vector store in a single batch operation.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  vector_store_id:
    description: ID of the vector store.
    type: str
    required: true
  file_ids:
    description: List of file IDs to add to the vector store.
    type: list
    elements: str
    required: true
"""

EXAMPLES = r"""
- name: Batch add files to vector store
  stevefulme1.openai.vector_store_file_batch:
    api_key: "{{ openai_api_key }}"
    vector_store_id: vs_abc123
    file_ids:
      - file-abc123
      - file-def456
  register: result
"""

RETURN = r"""
batch:
  description: The file batch object.
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
        vector_store_id=dict(type="str", required=True),
        file_ids=dict(type="list", elements="str", required=True),
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

    try:
        resp = client.post(
            "vector_stores/{}/file_batches".format(module.params["vector_store_id"]),
            data={"file_ids": module.params["file_ids"]},
        )
        module.exit_json(changed=True, batch=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Vector store file batch failed: {str(e)}")


if __name__ == "__main__":
    main()
