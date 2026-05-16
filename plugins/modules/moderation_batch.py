#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: moderation_batch
short_description: Run batch content moderation
description:
  - Run batch content moderation.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  inputs:
    description: List of text inputs to moderate.
    type: list
    elements: str
    required: true
  model:
    description: Moderation model to use.
    type: str
    required: false"""

EXAMPLES = r"""
- name: Run batch content moderation
  stevefulme1.openai.moderation_batch:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
results:
  description: Batch moderation results.
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
        inputs=dict(type="list", elements="str", required=True),
        model=dict(type="str", required=False),
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
        payload = {"input": module.params["inputs"]}
        if module.params.get("model"):
            payload["model"] = module.params["model"]

        resp = client.post("moderations", data=payload)
        module.exit_json(changed=True, results=resp)
    except OpenAIError as e:
        module.fail_json(msg="moderation_batch failed: %s" % str(e))


if __name__ == "__main__":
    main()
