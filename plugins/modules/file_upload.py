#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: file_upload
short_description: Upload a file to OpenAI
description:
  - Uploads a file to the OpenAI platform for use with assistants or fine-tuning.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  path:
    description: Local path to the file to upload.
    type: path
    required: true
  purpose:
    description: The intended purpose of the file.
    type: str
    choices: [assistants, fine-tune, batch, vision]
    required: true
"""

EXAMPLES = r"""
- name: Upload a training file
  stevefulme1.openai.file_upload:
    api_key: "{{ openai_api_key }}"
    path: /tmp/training.jsonl
    purpose: fine-tune
  register: result
"""

RETURN = r"""
file:
  description: The uploaded file object.
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
        path=dict(type="path", required=True),
        purpose=dict(
            type="str",
            required=True,
            choices=["assistants", "fine-tune", "batch", "vision"],
        ),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, file={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        resp = client.upload_file(
            "files",
            file_data=module.params["path"],
            purpose=module.params["purpose"],
        )
        module.exit_json(changed=True, file=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"File upload failed: {str(e)}")


if __name__ == "__main__":
    main()
