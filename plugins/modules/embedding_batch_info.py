#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: embedding_batch_info
short_description: Get OpenAI batch embedding job status
description:
  - Retrieves information about OpenAI batch.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  batch_id:
    description: ID of the batch embedding job.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Get OpenAI batch embedding job status
  stevefulme1.openai.embedding_batch_info:
    api_key: "{{ openai_api_key }}"
    batch_id: "example_batch_id"
  register: result
"""

RETURN = r"""
batch:
  description: The batch data.
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
    spec["batch_id"] = dict(type="str", required=True)

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
        resp = client.get("batches/{batch_id}".format(batch_id=module.params["batch_id"]))
        module.exit_json(changed=False, batch=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to retrieve batch: {str(e)}")


if __name__ == "__main__":
    main()
