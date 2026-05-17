#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: model_detail_info
short_description: Get details of a specific OpenAI model
description:
  - Retrieves detailed information about a specific OpenAI model.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model_id:
    description: The ID of the model to retrieve.
    type: str
    required: true
  limit:
    description:
      - Maximum number of results to return.
    type: int
    default: 100
  offset:
    description:
      - Number of results to skip for pagination.
    type: int
    default: 0
"""

EXAMPLES = r"""
- name: Get model details
  stevefulme1.openai.model_detail_info:
    api_key: "{{ openai_api_key }}"
    model_id: gpt-4
  register: result
"""

RETURN = r"""
model:
  description: Model details.
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
    spec["model_id"] = dict(type="str", required=True)
    spec["limit"] = dict(type="int", required=False, default=100)
    spec["offset"] = dict(type="int", required=False, default=0)

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
        resp = client.get("models/%s" % module.params["model_id"])
        module.exit_json(changed=False, model=resp)
    except OpenAIError as e:
        module.fail_json(msg="Failed to get model: %s" % str(e))


if __name__ == "__main__":
    main()
