#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: audio_speech
short_description: Generate speech from text with OpenAI TTS
description:
  - Converts text to speech using OpenAI's text-to-speech models.
  - This operation is inherently non-idempotent.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: The TTS model to use.
    type: str
    required: false
    default: tts-1
  input:
    description: The text to generate audio for.
    type: str
    required: true
  voice:
    description: The voice to use for generation.
    type: str
    choices: [alloy, echo, fable, onyx, nova, shimmer]
    required: true
  dest:
    description: Destination path to save the audio file.
    type: path
    required: true
  response_format:
    description: Audio format of the output.
    type: str
    choices: [mp3, opus, aac, flac, wav, pcm]
    required: false
  speed:
    description: Speed of the generated audio (0.25 to 4.0).
    type: float
    required: false
"""

EXAMPLES = r"""
- name: Generate speech
  stevefulme1.openai.audio_speech:
    api_key: "{{ openai_api_key }}"
    input: "Hello, welcome to OpenAI."
    voice: alloy
    dest: /tmp/speech.mp3
"""

RETURN = r"""
dest:
  description: Path to the saved audio file.
  type: str
  returned: always
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url
from ansible_collections.stevefulme1.openai.plugins.module_utils.openai_client import (
    openai_argument_spec,
)


def main():
    spec = openai_argument_spec()
    spec.update(
        model=dict(type="str", required=False, default="tts-1"),
        input=dict(type="str", required=True),
        voice=dict(
            type="str",
            required=True,
            choices=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        ),
        dest=dict(type="path", required=True),
        response_format=dict(
            type="str",
            required=False,
            choices=["mp3", "opus", "aac", "flac", "wav", "pcm"],
        ),
        speed=dict(type="float", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, dest=module.params["dest"])

    base_url = (module.params.get("base_url") or "https://api.openai.com/v1").rstrip("/")
    url = f"{base_url}/audio/speech"

    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json",
    }
    if module.params.get("organization"):
        headers["OpenAI-Organization"] = module.params["organization"]

    payload = dict(
        model=module.params["model"],
        input=module.params["input"],
        voice=module.params["voice"],
    )
    for opt in ("response_format", "speed"):
        if module.params.get(opt) is not None:
            payload[opt] = module.params[opt]

    try:
        resp = open_url(
            url,
            method="POST",
            data=json.dumps(payload),
            headers=headers,
            timeout=module.params["timeout"],
        )
        with open(module.params["dest"], "wb") as f:
            f.write(resp.read())
        module.exit_json(changed=True, dest=module.params["dest"])
    except Exception as e:
        module.fail_json(msg=f"Speech generation failed: {str(e)}")


if __name__ == "__main__":
    main()
