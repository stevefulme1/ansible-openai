#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: vector_store_file_info
short_description: List files in an OpenAI vector store
description:
  - Retrieves a list of files attached to a vector store.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  vector_store_id:
    description: ID of the vector store.
    type: str
    required: true
  limit:
    description: Maximum number of files to return.
    type: int
    required: false
    default: 100
  offset:
    description: Number of items to skip for pagination.
    type: int
    required: false
    default: 0
"""

EXAMPLES = r"""
- name: List vector store files
  stevefulme1.openai.vector_store_file_info:
    api_key: "{{ openai_api_key }}"
    vector_store_id: vs_abc123
  register: result
"""

RETURN = r"""
files:
  description: List of vector store file objects.
  type: list
  returned: always
  elements: dict
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
        limit=dict(type="int", required=False, default=20),
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
        data = client.list_paginated(
            "vector_stores/{}/files".format(module.params["vector_store_id"]),
            params={"limit": module.params["limit"]},
        )
        module.exit_json(changed=False, files=data)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to list vector store files: {str(e)}")


if __name__ == "__main__":
    main()
