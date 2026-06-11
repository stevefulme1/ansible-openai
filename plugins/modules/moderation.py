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
module: moderation
short_description: Manage moderations
version_added: "1.0.0"
description:
  - Create, update, and delete moderation resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the moderation resource.
    type: str
    choices: ['present', 'absent']
    default: present

  input:
    description:
      - >-
        A string of text to classify for moderation.
    type: str

    required: true

  model:
    description:
      - >-

    type: str

extends_documentation_fragment:
  - stevefulme1.openai.auth
"""

EXAMPLES = r"""

- name: Create a moderation
  stevefulme1.openai.moderation:

    input: "example_input"

    state: present
  # API: POST /moderations

- name: Update a moderation
  stevefulme1.openai.moderation:
    id: "existing_id"

    model: "updated_model"

    state: present
  # API:

"""

RETURN = r"""

flagged:
  description: >-
    Whether any of the below categories are flagged.
  returned: success
  type: bool

categories:
  description: >-
    A list of the categories, and whether they are flagged or not.
  returned: success
  type: dict

category_scores:
  description: >-
    A list of the categories along with their scores as predicted by model.
  returned: success
  type: dict

category_applied_input_types:
  description: >-
    A list of the categories along with the input type(s) that the score applies to.
  returned: success
  type: dict

"""


def get_current_state(client, module):
    """Retrieve the current state of the moderation via GET."""

    return None


def needs_update(current, desired):
    """Compare current state against desired params and return True if an update is needed."""
    if current is None:
        return True
    for key, value in desired.items():
        if value is None:
            continue
        current_value = current.get(key)
        if current_value != value:
            return True
    return False


def build_payload(module):
    """Build the API request payload from module params."""
    payload = {}

    if module.params.get("input") is not None:
        payload["input"] = module.params["input"]

    if module.params.get("model") is not None:
        payload["model"] = module.params["model"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            input=dict(
                type="str",

                required=True,



            ),

            model=dict(
                type="str",

            ),

        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,

    )

    state = module.params["state"]
    result = dict(changed=False, diff=dict(before={}, after={}))

    try:
        client = Client(module)
        current = get_current_state(client, module)

        if state == "present":
            desired = build_payload(module)

            if current is None:
                # Resource does not exist — create it
                result["changed"] = True
                result["diff"]["before"] = {}
                result["diff"]["after"] = desired

                if not module.check_mode:

                    response = client.POST(
                        "/moderations",
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            elif needs_update(current, desired):
                # Resource exists but needs updating
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = dict(current, **{k: v for k, v in desired.items() if v is not None})

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/moderations/{id}".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["flagged"] = current.get("flagged")

                result["categories"] = current.get("categories")

                result["category_scores"] = current.get("category_scores")

                result["category_applied_input_types"] = current.get("category_applied_input_types")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    pass

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
