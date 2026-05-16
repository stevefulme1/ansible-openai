#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: api_key_rotation
short_description: Automated API key rotation
description:
  - Automated API key rotation.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  old_key_id:
    description: ID of the key to rotate.
    type: str
    required: true
  project_id:
    description: Project scope for the new key.
    type: str
    required: false
  name:
    description: Name for the new key.
    type: str
    required: false"""

EXAMPLES = r"""
- name: Automated API key rotation
  stevefulme1.openai.api_key_rotation:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
api_key:
  description: The new API key after rotation.
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
        old_key_id=dict(type="str", required=True),
        project_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
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
            "rotate_key_id": module.params["old_key_id"],
        }
        if module.params.get("project_id"):
            payload["project_id"] = module.params["project_id"]
        if module.params.get("name"):
            payload["name"] = module.params["name"]

        resp = client.post("organization/api_keys", data=payload)
        module.exit_json(changed=True, api_key=resp)
    except OpenAIError as e:
        module.fail_json(msg="api_key_rotation failed: %s" % str(e))


if __name__ == "__main__":
    main()
