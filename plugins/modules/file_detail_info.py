#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: file_detail_info
short_description: Get metadata for a specific OpenAI file
description:
  - Retrieves metadata for a specific file uploaded to OpenAI.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  file_id:
    description: ID of the file to retrieve.
    type: str
    required: true
  limit:
    description:
      - Maximum number of results to return.
    type: int
    default: 100
  offset:
    description:
      - Number of results to skip for pagination.
    type: int
    default: 0
"""

EXAMPLES = r"""
- name: Get file details
  stevefulme1.openai.file_detail_info:
    api_key: "{{ openai_api_key }}"
    file_id: file-abc123
  register: result
"""

RETURN = r"""
file:
  description: The file metadata object.
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
    spec["file_id"] = dict(type="str", required=True)
    spec["limit"] = dict(type="int", required=False, default=100)
    spec["offset"] = dict(type="int", required=False, default=0)

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
        resp = client.get("files/{}".format(module.params["file_id"]))
        module.exit_json(changed=False, file=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to get file: {str(e)}")


if __name__ == "__main__":
    main()
