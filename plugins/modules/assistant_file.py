#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: assistant_file
short_description: Manage files attached to assistants
description:
  - Manage files attached to assistants.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the file attachment.
    type: str
    choices: [present, absent]
    default: present
  assistant_id:
    description: ID of the assistant.
    type: str
    required: true
  file_id:
    description: ID of the file to attach or detach.
    type: str
    required: true"""

EXAMPLES = r"""
- name: Manage files attached to assistants
  stevefulme1.openai.assistant_file:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
file:
  description: The assistant file object.
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
        state=dict(type="str", choices=["present", "absent"], default="present"),
        assistant_id=dict(type="str", required=True),
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

    try:
        payload = {"file_id": module.params["file_id"]}

        aid = module.params["assistant_id"]
        fid = module.params["file_id"]
        if module.params["state"] == "absent":
            resp = client.delete("assistants/%s/files/%s" % (aid, fid))
            module.exit_json(changed=True, file=resp)
            return
        endpoint = "assistants/%s/files" % aid
        resp = client.post(endpoint, data=payload)
        module.exit_json(changed=True, file=resp)
    except OpenAIError as e:
        module.fail_json(msg="assistant_file failed: %s" % str(e))


if __name__ == "__main__":
    main()
