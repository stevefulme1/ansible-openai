#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r"""
---
module: vector_store
short_description: Manage vector stores
version_added: "1.0.0"
description:
  - Create, update, and delete vector_store resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the vector_store resource.
    type: str
    choices: ['present', 'absent']
    default: present

  chunking_strategy:
    description:
      - >-
        The default strategy. This strategy currently uses a max_chunk_size_tokens of 800 and...
    type: dict

  description:
    description:
      - >-
        A description for the vector store. Can be used to describe the vector store's purpose.
    type: str

  expires_after:
    description:
      - >-
        The expiration policy for a vector store.
    type: dict

  file_ids:
    description:
      - >-
        A list of File(/docs/api-reference/files) IDs that the vector store should use. Useful for tools...
    type: list
    elements: str

  metadata:
    description:
      - >-
        Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
    type: dict

  name:
    description:
      - >-
        The name of the vector store.
    type: str

extends_documentation_fragment:
  - stevefulme1.openai.auth
"""

EXAMPLES = r"""

- name: Create a vector_store
  stevefulme1.openai.vector_store:

    state: present
  # API: POST /vector_stores/{vector_store_id}

- name: Update a vector_store
  stevefulme1.openai.vector_store:
    id: "existing_id"

    chunking_strategy: "updated_chunking_strategy"

    description: "updated_description"

    expires_after: "updated_expires_after"

    file_ids: "updated_file_ids"

    metadata: "updated_metadata"

    name: "updated_name"

    state: present
  # API:

- name: Delete a vector_store
  stevefulme1.openai.vector_store:
    id: "existing_id"
    state: absent
  # API: DELETE /vector_stores/{vector_store_id}

"""

RETURN = r"""

id:
  description: >-
    The identifier, which can be referenced in API endpoints.
  returned: success
  type: str

object:
  description: >-
    The object type, which is always vector_store.
  returned: success
  type: str

created_at:
  description: >-
    The Unix timestamp (in seconds) for when the vector store was created.
  returned: success
  type: int

name:
  description: >-
    The name of the vector store.
  returned: success
  type: str

usage_bytes:
  description: >-
    The total number of bytes used by the files in the vector store.
  returned: success
  type: int

file_counts:
  description: >-

  returned: success
  type: dict

status:
  description: >-
    The status of the vector store, which can be either expired, in_progress, or completed. A status...
  returned: success
  type: str

expires_after:
  description: >-
    The expiration policy for a vector store.
  returned: success
  type: dict

expires_at:
  description: >-
    The Unix timestamp (in seconds) for when the vector store will expire.
  returned: success
  type: int

last_active_at:
  description: >-
    The Unix timestamp (in seconds) for when the vector store was last active.
  returned: success
  type: int

metadata:
  description: >-
    Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
  returned: success
  type: dict

"""

from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule

def get_current_state(client, module):
    """Retrieve the current state of the vector_store via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/vector_stores")
        if isinstance(items, dict):
            items = items.get("results", items.get("data", items.get("items", [])))
        for item in items:
            if str(item.get(search_key)) == str(search_value):
                return item
            if str(item.get("id")) == str(search_value):
                return item
        return None
    except ClientError:
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

    if module.params.get("chunking_strategy") is not None:
        payload["chunking_strategy"] = module.params["chunking_strategy"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("expires_after") is not None:
        payload["expires_after"] = module.params["expires_after"]

    if module.params.get("file_ids") is not None:
        payload["file_ids"] = module.params["file_ids"]

    if module.params.get("metadata") is not None:
        payload["metadata"] = module.params["metadata"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            chunking_strategy=dict(
                type="dict",

            ),

            description=dict(
                type="str",

            ),

            expires_after=dict(
                type="dict",

            ),

            file_ids=dict(
                type="list",
                elements="str",

            ),

            metadata=dict(
                type="dict",

            ),

            name=dict(
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
                        "/vector_stores/{vector_store_id}",
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
                    path = "/vector_stores/{id}".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["id"] = current.get("id")

                result["object"] = current.get("object")

                result["created_at"] = current.get("created_at")

                result["name"] = current.get("name")

                result["usage_bytes"] = current.get("usage_bytes")

                result["file_counts"] = current.get("file_counts")

                result["status"] = current.get("status")

                result["expires_after"] = current.get("expires_after")

                result["expires_at"] = current.get("expires_at")

                result["last_active_at"] = current.get("last_active_at")

                result["metadata"] = current.get("metadata")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/vector_stores/{id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
