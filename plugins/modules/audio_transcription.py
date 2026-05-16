#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: audio_transcription
short_description: Transcribe audio with OpenAI Whisper
description:
  - Transcribes audio into text using the Whisper model.
  - This operation is inherently non-idempotent.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  file:
    description: Path to the audio file to transcribe.
    type: path
    required: true
  model:
    description: The model to use for transcription.
    type: str
    required: false
    default: whisper-1
  language:
    description: Language of the audio in ISO-639-1 format.
    type: str
    required: false
  response_format:
    description: Output format for the transcription.
    type: str
    choices: [json, text, srt, verbose_json, vtt]
    required: false
  temperature:
    description: Sampling temperature between 0 and 1.
    type: float
    required: false
"""

EXAMPLES = r"""
- name: Transcribe audio
  stevefulme1.openai.audio_transcription:
    api_key: "{{ openai_api_key }}"
    file: /tmp/audio.mp3
  register: result
"""

RETURN = r"""
transcription:
  description: The transcription result.
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
        file=dict(type="path", required=True),
        model=dict(type="str", required=False, default="whisper-1"),
        language=dict(type="str", required=False),
        response_format=dict(
            type="str",
            required=False,
            choices=["json", "text", "srt", "verbose_json", "vtt"],
        ),
        temperature=dict(type="float", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, transcription={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    extra = {"model": module.params["model"]}
    for opt in ("language", "response_format", "temperature"):
        if module.params.get(opt) is not None:
            extra[opt] = str(module.params[opt])

    try:
        resp = client.upload_file(
            "audio/transcriptions",
            file_data=module.params["file"],
            purpose="audio",
            extra_fields=extra,
        )
        module.exit_json(changed=True, transcription=resp)
    except OpenAIError as e:
        module.fail_json(msg="Audio transcription failed: %s" % str(e))


if __name__ == "__main__":
    main()
