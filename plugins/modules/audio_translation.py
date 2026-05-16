#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: audio_translation
short_description: Translate audio to English with OpenAI Whisper
description:
  - Translates audio into English text using the Whisper model.
  - This operation is inherently non-idempotent.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  file:
    description: Path to the audio file to translate.
    type: path
    required: true
  model:
    description: The model to use for translation.
    type: str
    required: false
    default: whisper-1
  response_format:
    description: Output format for the translation.
    type: str
    choices: [json, text, srt, verbose_json, vtt]
    required: false
"""

EXAMPLES = r"""
- name: Translate audio to English
  stevefulme1.openai.audio_translation:
    api_key: "{{ openai_api_key }}"
    file: /tmp/french_audio.mp3
  register: result
"""

RETURN = r"""
translation:
  description: The translation result.
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
        response_format=dict(
            type="str",
            required=False,
            choices=["json", "text", "srt", "verbose_json", "vtt"],
        ),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, translation={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    extra = {"model": module.params["model"]}
    if module.params.get("response_format"):
        extra["response_format"] = module.params["response_format"]

    try:
        resp = client.upload_file(
            "audio/translations",
            file_data=module.params["file"],
            purpose="audio",
            extra_fields=extra,
        )
        module.exit_json(changed=True, translation=resp)
    except OpenAIError as e:
        module.fail_json(msg="Audio translation failed: %s" % str(e))


if __name__ == "__main__":
    main()
