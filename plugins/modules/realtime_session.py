#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: realtime_session
short_description: Create a realtime session
description:
  - Create a realtime session.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: Model for the realtime session.
    type: str
    required: true
  modalities:
    description: Session modalities (text, audio).
    type: list
    elements: str
    required: false
  voice:
    description: Voice for audio output.
    type: str
    required: false"""

EXAMPLES = r"""
- name: Create a realtime session
  stevefulme1.openai.realtime_session:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
session:
  description: The realtime session object.
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
        modalities=dict(type="list", elements="str", required=False),
        voice=dict(type="str", required=False),
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
        for opt in ("modalities", "voice"):
            if module.params.get(opt) is not None:
                payload[opt] = module.params[opt]

        resp = client.post("realtime/sessions", data=payload)
        module.exit_json(changed=True, session=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"realtime_session failed: {str(e)}")


if __name__ == "__main__":
    main()
