#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: vector_store
short_description: Create, update, or delete an OpenAI vector store
description:
  - Manages OpenAI vector store lifecycle.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the vector store.
    type: str
    choices: [present, absent]
    default: present
  vector_store_id:
    description: ID of the vector store (required for update/delete).
    type: str
    required: false
  name:
    description: Name of the vector store.
    type: str
    required: false
  file_ids:
    description: List of file IDs to attach.
    type: list
    elements: str
    required: false
  expires_after:
    description: Expiration policy.
    type: dict
    required: false
  metadata:
    description: Metadata key-value pairs.
    type: dict
    required: false
"""

EXAMPLES = r"""
- name: Create a vector store
  stevefulme1.openai.vector_store:
    api_key: "{{ openai_api_key }}"
    name: "Knowledge Base"
  register: result

- name: Delete a vector store
  stevefulme1.openai.vector_store:
    api_key: "{{ openai_api_key }}"
    vector_store_id: vs_abc123
    state: absent
"""

RETURN = r"""
vector_store:
  description: The vector store object.
  type: dict
  returned: when state is present
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
        state=dict(type="str", choices=["present", "absent"], default="present"),
        vector_store_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        file_ids=dict(type="list", elements="str", required=False),
        expires_after=dict(type="dict", required=False),
        metadata=dict(type="dict", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_if=[("state", "absent", ["vector_store_id"])],
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
        if module.params["state"] == "absent":
            client.delete("vector_stores/{}".format(module.params["vector_store_id"]))
            module.exit_json(changed=True)
        else:
            payload = {}
            for opt in ("name", "file_ids", "expires_after", "metadata"):
                if module.params.get(opt) is not None:
                    payload[opt] = module.params[opt]

            if module.params.get("vector_store_id"):
                resp = client.post(
                    "vector_stores/{}".format(module.params["vector_store_id"]),
                    data=payload,
                )
            else:
                resp = client.post("vector_stores", data=payload)
            module.exit_json(changed=True, vector_store=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Vector store operation failed: {str(e)}")


if __name__ == "__main__":
    main()
