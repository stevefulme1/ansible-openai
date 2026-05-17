#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: realtime_token
short_description: Generate ephemeral realtime token
description:
  - Generate ephemeral realtime token.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: Model for the token.
    type: str
    required: true
  expires_after:
    description: Token expiration in seconds.
    type: int
    required: false"""

EXAMPLES = r"""
- name: Generate ephemeral realtime token
  stevefulme1.openai.realtime_token:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
token:
  description: The ephemeral token.
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
        expires_after=dict(type="int", required=False),
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
        payload = {"model": module.params["model"]}
        if module.params.get("expires_after") is not None:
            payload["expires_after"] = module.params["expires_after"]

        resp = client.post("realtime/sessions", data=payload)
        module.exit_json(changed=True, token=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"realtime_token failed: {str(e)}")


if __name__ == "__main__":
    main()
