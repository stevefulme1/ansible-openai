#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: image_generate
short_description: Generate images with OpenAI DALL-E
description:
  - Creates images from a text prompt using DALL-E.
  - This operation is inherently non-idempotent.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  prompt:
    description: Text description of the desired image.
    type: str
    required: true
  model:
    description: The model to use for image generation.
    type: str
    required: false
    default: dall-e-3
  n:
    description: Number of images to generate.
    type: int
    required: false
    default: 1
  size:
    description: Size of the generated image.
    type: str
    choices: ['256x256', '512x512', '1024x1024', '1792x1024', '1024x1792']
    required: false
    default: '1024x1024'
  quality:
    description: Quality of the generated image.
    type: str
    choices: [standard, hd]
    required: false
  response_format:
    description: Format of the response.
    type: str
    choices: [url, b64_json]
    required: false
"""

EXAMPLES = r"""
- name: Generate an image
  stevefulme1.openai.image_generate:
    api_key: "{{ openai_api_key }}"
    prompt: "A sunset over mountains"
  register: result
"""

RETURN = r"""
images:
  description: The generated image data.
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
        prompt=dict(type="str", required=True),
        model=dict(type="str", required=False, default="dall-e-3"),
        n=dict(type="int", required=False, default=1),
        size=dict(
            type="str",
            required=False,
            default="1024x1024",
            choices=["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"],
        ),
        quality=dict(type="str", required=False, choices=["standard", "hd"]),
        response_format=dict(type="str", required=False, choices=["url", "b64_json"]),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, images={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    payload = dict(
        prompt=module.params["prompt"],
        model=module.params["model"],
        n=module.params["n"],
        size=module.params["size"],
    )
    for opt in ("quality", "response_format"):
        if module.params.get(opt) is not None:
            payload[opt] = module.params[opt]

    try:
        resp = client.post("images/generations", data=payload)
        module.exit_json(changed=True, images=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Image generation failed: {str(e)}")


if __name__ == "__main__":
    main()
