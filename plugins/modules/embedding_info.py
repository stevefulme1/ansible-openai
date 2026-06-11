#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = r"""
---
module: embedding_info
short_description: Retrieve information about embedding resources
version_added: "1.0.0"
description:
  - Retrieve a single embedding by its identifier, or list all embedding resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the embedding to retrieve.
      - When omitted, all embedding resources are listed.
    type: str
    required: false

  page:
    description:
      - Page number for paginated results.
      - Only applies when listing resources.
    type: int
    required: false
  page_size:
    description:
      - Number of results per page.
      - Only applies when listing resources.
    type: int
    required: false
extends_documentation_fragment:
  - stevefulme1.openai.auth
"""

EXAMPLES = r"""
- name: Get a specific embedding
  stevefulme1.openai.embedding_info:
    id: "example_id"
  register: result

- name: List all embedding resources
  stevefulme1.openai.embedding_info:
  register: result

- name: List embedding resources with pagination
  stevefulme1.openai.embedding_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
embeddings:
  description: List of embedding resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    index:
      description: >-
        The index of the embedding in the list of embeddings.
      type: int

    embedding:
      description: >-
        The embedding vector, which is a list of floats. The length of vector depends on the model as...
      type: list

    object:
      description: >-
        The object type, which is always "embedding".
      type: str

"""


def fetch_single(client, identifier):
    """Retrieve a single embedding by identifier."""

    raise ClientError("GET by identifier is not supported for this resource")


def fetch_list(client, module):
    """List embedding resources with optional filtering and pagination."""

    raise ClientError("List operation is not supported for this resource")


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            id=dict(type="str", required=False),

            page=dict(type="int", required=False),
            page_size=dict(type="int", required=False),
        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ("id", "page"),
            ("id", "page_size"),
        ],
    )

    result = dict(
        changed=False,
        embeddings=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["embeddings"] = [item] if item else []
        else:
            result["embeddings"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
