#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: batch_info
short_description: List or get details of OpenAI batch jobs
description:
  - Retrieves batch job information. Lists all batches or gets a specific one.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  batch_id:
    description: ID of a specific batch to retrieve.
    type: str
    required: false
  limit:
    description: Maximum number of batches to return.
    type: int
    required: false
    default: 20
"""

EXAMPLES = r"""
- name: List all batches
  stevefulme1.openai.batch_info:
    api_key: "{{ openai_api_key }}"
  register: result

- name: Get a specific batch
  stevefulme1.openai.batch_info:
    api_key: "{{ openai_api_key }}"
    batch_id: batch_abc123
  register: result
"""

RETURN = r"""
batch:
  description: A single batch object (when batch_id is provided).
  type: dict
  returned: when batch_id is provided
batches:
  description: List of batch objects.
  type: list
  returned: when batch_id is not provided
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
    spec.update(
        batch_id=dict(type="str", required=False),
        limit=dict(type="int", required=False, default=20),
    )

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
        if module.params.get("batch_id"):
            resp = client.get("batches/%s" % module.params["batch_id"])
            module.exit_json(changed=False, batch=resp)
        else:
            data = client.list_paginated(
                "batches", params={"limit": module.params["limit"]}
            )
            module.exit_json(changed=False, batches=data)
    except OpenAIError as e:
        module.fail_json(msg="Failed to get batch info: %s" % str(e))


if __name__ == "__main__":
    main()
