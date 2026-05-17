#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: embedding_dimension
short_description: Configure embedding dimensions
description:
  - Configure embedding dimensions.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: Embedding model to use.
    type: str
    required: true
  input:
    description: Text to embed.
    type: raw
    required: true
  dimensions:
    description: Number of output dimensions.
    type: int
    required: true"""

EXAMPLES = r"""
- name: Configure embedding dimensions
  stevefulme1.openai.embedding_dimension:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
embedding:
  description: The embedding with configured dimensions.
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
        model=dict(type="str", required=True),
        input=dict(type="raw", required=True),
        dimensions=dict(type="int", required=True),
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
        payload = {
            "model": module.params["model"],
            "input": module.params["input"],
            "dimensions": module.params["dimensions"],
        }

        resp = client.post("embeddings", data=payload)
        module.exit_json(changed=True, embedding=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"embedding_dimension failed: {str(e)}")


if __name__ == "__main__":
    main()
