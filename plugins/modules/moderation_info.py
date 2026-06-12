#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r"""
---
module: moderation_info
short_description: Retrieve information about moderation resources
version_added: "1.0.0"
description:
  - Retrieve a single moderation by its identifier, or list all moderation resources.
  - This module always reports C(changed=False).
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  id:
    description:
      - The unique identifier of the moderation to retrieve.
      - When omitted, all moderation resources are listed.
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
- name: Get a specific moderation
  stevefulme1.openai.moderation_info:
    id: "example_id"
  register: result

- name: List all moderation resources
  stevefulme1.openai.moderation_info:
  register: result

- name: List moderation resources with pagination
  stevefulme1.openai.moderation_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
moderations:
  description: List of moderation resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    flagged:
      description: >-
        Whether any of the below categories are flagged.
      type: bool

    categories:
      description: >-
        A list of the categories, and whether they are flagged or not.
      type: dict

    category_scores:
      description: >-
        A list of the categories along with their scores as predicted by model.
      type: dict

    category_applied_input_types:
      description: >-
        A list of the categories along with the input type(s) that the score applies to.
      type: dict

"""

from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule

def fetch_single(client, identifier):
    """Retrieve a single moderation by identifier."""

    raise ClientError("GET by identifier is not supported for this resource")


def fetch_list(client, module):
    """List moderation resources with optional filtering and pagination."""

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
        moderations=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("id")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["moderations"] = [item] if item else []
        else:
            result["moderations"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
