#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: image_edit
short_description: Edit an image with OpenAI DALL-E
description:
  - Edits an existing image given a prompt and mask.
  - This operation is inherently non-idempotent.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  image:
    description: Path to the image file to edit.
    type: path
    required: true
  prompt:
    description: Text description of the desired edit.
    type: str
    required: true
  mask:
    description: Path to the mask image file.
    type: path
    required: false
  n:
    description: Number of images to generate.
    type: int
    required: false
    default: 1
  size:
    description: Size of the generated image.
    type: str
    choices: ['256x256', '512x512', '1024x1024']
    required: false
    default: '1024x1024'
"""

EXAMPLES = r"""
- name: Edit an image
  stevefulme1.openai.image_edit:
    api_key: "{{ openai_api_key }}"
    image: /tmp/original.png
    prompt: "Add a hat to the person"
  register: result
"""

RETURN = r"""
images:
  description: The edited image data.
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
        image=dict(type="path", required=True),
        prompt=dict(type="str", required=True),
        mask=dict(type="path", required=False),
        n=dict(type="int", required=False, default=1),
        size=dict(
            type="str",
            required=False,
            default="1024x1024",
            choices=["256x256", "512x512", "1024x1024"],
        ),
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

    try:
        resp = client.upload_file(
            "images/edits",
            file_data=module.params["image"],
            purpose="image",
            extra_fields={
                "prompt": module.params["prompt"],
                "n": str(module.params["n"]),
                "size": module.params["size"],
            },
        )
        module.exit_json(changed=True, images=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Image edit failed: {str(e)}")


if __name__ == "__main__":
    main()
