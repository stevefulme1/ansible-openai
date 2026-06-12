#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r"""
---
module: embedding
short_description: Manage embeddings
version_added: "1.0.0"
description:
  - Create, update, and delete embedding resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the embedding resource.
    type: str
    choices: ['present', 'absent']
    default: present

  input:
    description:
      - >-
        The string that will be turned into an embedding.
    type: str

    required: true

  model:
    description:
      - >-

    type: str

    required: true

  dimensions:
    description:
      - >-
        The number of dimensions the resulting output embeddings should have. Only supported in...
    type: int

  encoding_format:
    description:
      - >-
        The format to return the embeddings in. Can be either float or base64.
    type: str

    choices: ["float", "base64"]

    default: "float"

  user:
    description:
      - >-
        A unique identifier representing your end-user, which can help OpenAI to monitor and detect...
    type: str

extends_documentation_fragment:
  - stevefulme1.openai.auth
"""

EXAMPLES = r"""

- name: Create a embedding
  stevefulme1.openai.embedding:

    input: "example_input"

    model: "example_model"

    state: present
  # API: POST /embeddings

- name: Update a embedding
  stevefulme1.openai.embedding:
    id: "existing_id"

    dimensions: "updated_dimensions"

    encoding_format: "updated_encoding_format"

    user: "updated_user"

    state: present
  # API:

"""

RETURN = r"""

index:
  description: >-
    The index of the embedding in the list of embeddings.
  returned: success
  type: int

embedding:
  description: >-
    The embedding vector, which is a list of floats. The length of vector depends on the model as...
  returned: success
  type: list

object:
  description: >-
    The object type, which is always "embedding".
  returned: success
  type: str

"""

from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule


def get_current_state(client, module):
    """Retrieve the current state of the embedding via GET."""

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

    if module.params.get("dimensions") is not None:
        payload["dimensions"] = module.params["dimensions"]

    if module.params.get("encoding_format") is not None:
        payload["encoding_format"] = module.params["encoding_format"]

    if module.params.get("user") is not None:
        payload["user"] = module.params["user"]

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

                required=True,

            ),

            dimensions=dict(
                type="int",

            ),

            encoding_format=dict(
                type="str",

                choices=['float', 'base64'],

                default="float",

            ),

            user=dict(
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
                        "/embeddings",
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
                    path = "/embeddings/{id}".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["index"] = current.get("index")

                result["embedding"] = current.get("embedding")

                result["object"] = current.get("object")

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
