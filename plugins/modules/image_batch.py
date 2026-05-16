#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: image_batch
short_description: Batch image generation
description:
  - Batch image generation.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  prompts:
    description: List of prompts for image generation.
    type: list
    elements: str
    required: true
  model:
    description: Image model to use.
    type: str
    default: dall-e-3
  size:
    description: Image size.
    type: str
    default: 1024x1024"""

EXAMPLES = r"""
- name: Batch image generation
  stevefulme1.openai.image_batch:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
images:
  description: Generated images.
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
        prompts=dict(type="list", elements="str", required=True),
        model=dict(type="str", default="dall-e-3"),
        size=dict(type="str", default="1024x1024"),
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
        for prompt in module.params["prompts"]:
            payload = {
                "model": module.params["model"],
                "prompt": prompt,
                "size": module.params["size"],
                "n": 1,
            }
            r = client.post("images/generations", data=payload)
            results.append(r)
        module.exit_json(changed=True, images=results)
        return

        pass  # handled above
    except OpenAIError as e:
        module.fail_json(msg="image_batch failed: %s" % str(e))


if __name__ == "__main__":
    main()
