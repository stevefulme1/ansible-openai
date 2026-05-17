#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: assistant_vector_store
short_description: Attach vector store to assistant
description:
  - Attach vector store to assistant.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  assistant_id:
    description: ID of the assistant.
    type: str
    required: true
  vector_store_ids:
    description: List of vector store IDs to attach.
    type: list
    elements: str
    required: true"""

EXAMPLES = r"""
- name: Attach vector store to assistant
  stevefulme1.openai.assistant_vector_store:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
assistant:
  description: The updated assistant object.
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
        assistant_id=dict(type="str", required=True),
        vector_store_ids=dict(type="list", elements="str", required=True),
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
        payload = {"tool_resources": {"file_search": {"vector_store_ids": module.params["vector_store_ids"]}}}

        endpoint = "assistants/{}".format(module.params["assistant_id"])
        resp = client.post(endpoint, data=payload)
        module.exit_json(changed=True, assistant=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"assistant_vector_store failed: {str(e)}")


if __name__ == "__main__":
    main()
