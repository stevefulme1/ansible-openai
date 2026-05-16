#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: embedding_batch
short_description: Batch create OpenAI embeddings
description:
  - Generates vector embeddings for multiple input texts in a single call.
  - This operation is inherently non-idempotent.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: ID of the embedding model to use.
    type: str
    required: true
  inputs:
    description: List of texts to generate embeddings for.
    type: list
    elements: str
    required: true
  encoding_format:
    description: Encoding format for the embeddings.
    type: str
    choices: [float, base64]
    required: false
"""

EXAMPLES = r"""
- name: Create batch embeddings
  stevefulme1.openai.embedding_batch:
    api_key: "{{ openai_api_key }}"
    model: text-embedding-3-small
    inputs:
      - "First text"
      - "Second text"
  register: result
"""

RETURN = r"""
embedding:
  description: The embedding response with multiple vectors.
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
        model=dict(type="str", required=True),
        inputs=dict(type="list", elements="str", required=True),
        encoding_format=dict(type="str", required=False, choices=["float", "base64"]),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, embedding={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    payload = dict(
        model=module.params["model"],
        input=module.params["inputs"],
    )
    if module.params.get("encoding_format"):
        payload["encoding_format"] = module.params["encoding_format"]

    try:
        resp = client.post("embeddings", data=payload)
        module.exit_json(changed=True, embedding=resp)
    except OpenAIError as e:
        module.fail_json(msg="Batch embedding creation failed: %s" % str(e))


if __name__ == "__main__":
    main()
