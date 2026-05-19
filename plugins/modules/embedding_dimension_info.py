#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: embedding_dimension_info
short_description: Get supported dimensions for an OpenAI embedding model
description:
  - Retrieves information about OpenAI model.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: ID of the embedding model.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Get supported dimensions for an OpenAI embedding model
  stevefulme1.openai.embedding_dimension_info:
    api_key: "{{ openai_api_key }}"
    model: "example_model"
  register: result
"""

RETURN = r"""
model:
  description: The model data.
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
    spec["model"] = dict(type="str", required=True)

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
        resp = client.get("models/{model}".format(model=module.params["model"]))
        module.exit_json(changed=False, model=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to retrieve model: {str(e)}")


if __name__ == "__main__":
    main()
