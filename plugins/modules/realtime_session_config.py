#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: realtime_session_config
short_description: Configure realtime session parameters
description:
  - Configure realtime session parameters.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  session_id:
    description: ID of the realtime session.
    type: str
    required: true
  turn_detection:
    description: Turn detection configuration.
    type: dict
    required: false
  input_audio_format:
    description: Input audio format.
    type: str
    required: false
  output_audio_format:
    description: Output audio format.
    type: str
    required: false"""

EXAMPLES = r"""
- name: Configure realtime session parameters
  stevefulme1.openai.realtime_session_config:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
config:
  description: The session configuration.
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
        session_id=dict(type="str", required=True),
        turn_detection=dict(type="dict", required=False),
        input_audio_format=dict(type="str", required=False),
        output_audio_format=dict(type="str", required=False),
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
        payload = {}
        for opt in ("turn_detection", "input_audio_format", "output_audio_format"):
            if module.params.get(opt) is not None:
                payload[opt] = module.params[opt]

        endpoint = "realtime/sessions/{}".format(module.params["session_id"])
        resp = client.post(endpoint, data=payload)
        module.exit_json(changed=True, config=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"realtime_session_config failed: {str(e)}")


if __name__ == "__main__":
    main()
