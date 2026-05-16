#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vector_store_file
short_description: Add or remove a file from an OpenAI vector store
description:
  - Manages files within a vector store.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the file in the vector store.
    type: str
    choices: [present, absent]
    default: present
  vector_store_id:
    description: ID of the vector store.
    type: str
    required: true
  file_id:
    description: ID of the file to add or remove.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Add a file to a vector store
  stevefulme1.openai.vector_store_file:
    api_key: "{{ openai_api_key }}"
    vector_store_id: vs_abc123
    file_id: file-abc123
"""

RETURN = r"""
vector_store_file:
  description: The vector store file object.
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
        vector_store_id=dict(type="str", required=True),
        file_id=dict(type="str", required=True),
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

    vs_id = module.params["vector_store_id"]
    file_id = module.params["file_id"]

    try:
        if module.params["state"] == "absent":
            client.delete("vector_stores/%s/files/%s" % (vs_id, file_id))
            module.exit_json(changed=True)
        else:
            resp = client.post(
                "vector_stores/%s/files" % vs_id,
                data={"file_id": file_id},
            )
            module.exit_json(changed=True, vector_store_file=resp)
    except OpenAIError as e:
        module.fail_json(msg="Vector store file operation failed: %s" % str(e))


if __name__ == "__main__":
    main()
