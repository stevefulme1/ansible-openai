#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: audio_batch_transcription
short_description: Batch audio transcription
description:
  - Batch audio transcription.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  file_ids:
    description: List of audio file IDs to transcribe.
    type: list
    elements: str
    required: true
  model:
    description: Transcription model.
    type: str
    default: whisper-1"""

EXAMPLES = r"""
- name: Batch audio transcription
  stevefulme1.openai.audio_batch_transcription:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
transcriptions:
  description: Batch transcription results.
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
        file_ids=dict(type="list", elements="str", required=True),
        model=dict(type="str", default="whisper-1"),
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
        results = []
        for fid in module.params["file_ids"]:
            payload = {
                "model": module.params["model"],
                "file": fid,
            }
            r = client.post("audio/transcriptions", data=payload)
            results.append(r)
        module.exit_json(changed=True, transcriptions=results)
    except OpenAIError as e:
        module.fail_json(msg=f"audio_batch_transcription failed: {str(e)}")


if __name__ == "__main__":
    main()
