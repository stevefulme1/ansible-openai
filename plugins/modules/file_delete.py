#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: file_delete
short_description: Delete an OpenAI file
description:
  - Deletes a file from the OpenAI platform.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  file_id:
    description: ID of the file to delete.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Delete a file
  stevefulme1.openai.file_delete:
    api_key: "{{ openai_api_key }}"
    file_id: file-abc123
"""

RETURN = r"""
deleted:
  description: Whether the file was deleted.
  type: bool
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
        resp = client.delete("files/{}".format(module.params["file_id"]))
        module.exit_json(changed=True, deleted=resp.get("deleted", True))
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to delete file: {str(e)}")


if __name__ == "__main__":
    main()
