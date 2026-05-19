#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: audio_speech_info
short_description: List available OpenAI text-to-speech voices
description:
  - Retrieves information about OpenAI voices.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  limit:
    description: Maximum number of results to return.
    type: int
    required: false
    default: 100
"""

EXAMPLES = r"""
- name: List available OpenAI text-to-speech voices
  stevefulme1.openai.audio_speech_info:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
voices:
  description: The voices data.
  type: list
  returned: always
  elements: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.openai.plugins.module_utils.openai_client import (
    OpenAIClient,
    OpenAIError,
    openai_argument_spec,
)


def main():
    spec = openai_argument_spec()

    spec["limit"] = dict(type="int", required=False, default=100)

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
        data = client.list_paginated("audio/voices", params={"limit": module.params["limit"]})
        module.exit_json(changed=False, voices=data)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to retrieve voices: {str(e)}")


if __name__ == "__main__":
    main()
