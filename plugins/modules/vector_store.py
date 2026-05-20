#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: vector_store
short_description: Create, update, or delete an OpenAI vector store
description:
  - Manages OpenAI vector store lifecycle.
  - Idempotent -- a second run with identical parameters returns changed=False.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the vector store.
    type: str
    choices: [present, absent]
    default: present
  vector_store_id:
    description: ID of the vector store (required for update/delete).
    type: str
    required: false
  name:
    description: Name of the vector store. Used for lookup when vector_store_id is not provided.
    type: str
    required: false
  file_ids:
    description: List of file IDs to attach.
    type: list
    elements: str
    required: false
  expires_after:
    description: Expiration policy.
    type: dict
    required: false
  metadata:
    description: Metadata key-value pairs.
    type: dict
    required: false
"""

EXAMPLES = r"""
- name: Create a vector store
  stevefulme1.openai.vector_store:
    api_key: "{{ openai_api_key }}"
    name: "Knowledge Base"
  register: result

- name: Update metadata
  stevefulme1.openai.vector_store:
    api_key: "{{ openai_api_key }}"
    vector_store_id: vs_abc123
    metadata:
      project: docs

- name: Delete a vector store
  stevefulme1.openai.vector_store:
    api_key: "{{ openai_api_key }}"
    vector_store_id: vs_abc123
    state: absent
"""

RETURN = r"""
vector_store:
  description: The vector store object.
  type: dict
  returned: when state is present
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.openai.plugins.module_utils.openai_client import (
    OpenAIClient,
    OpenAIError,
    openai_argument_spec,
)

COMPARE_KEYS = ("name", "expires_after", "metadata")


def get_current_state(client, module):
    """GET the vector store, return None if not found."""
    vs_id = module.params.get("vector_store_id")
    if vs_id:
        try:
            return client.get("vector_stores/{0}".format(vs_id))
        except OpenAIError as e:
            if e.status_code == 404:
                return None
            raise
    name = module.params.get("name")
    if name:
        stores = client.list_paginated("vector_stores")
        for vs in stores:
            if vs.get("name") == name:
                return vs
    return None


def needs_update(current, desired):
    """Compare current state with desired parameters, return dict of changes."""
    changes = {}
    for key in COMPARE_KEYS:
        if desired.get(key) is not None:
            if current.get(key) != desired[key]:
                changes[key] = desired[key]
    return changes


def build_desired(module):
    """Build desired-state dict from module params."""
    desired = {}
    for key in ("name", "file_ids", "expires_after", "metadata"):
        if module.params.get(key) is not None:
            desired[key] = module.params[key]
    return desired


def main():
    spec = openai_argument_spec()
    spec.update(
        state=dict(type="str", choices=["present", "absent"], default="present"),
        vector_store_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        file_ids=dict(type="list", elements="str", required=False),
        expires_after=dict(type="dict", required=False),
        metadata=dict(type="dict", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("vector_store_id", "name"), True),
        ],
    )

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    state = module.params["state"]

    try:
        current = get_current_state(client, module)

        if state == "absent":
            if current is None:
                module.exit_json(changed=False)
            if module.check_mode:
                module.exit_json(changed=True)
            client.delete("vector_stores/{0}".format(current["id"]))
            module.exit_json(changed=True)
        else:
            desired = build_desired(module)
            if current:
                changes = needs_update(current, desired)
                if not changes:
                    module.exit_json(changed=False, vector_store=current)
                if module.check_mode:
                    module.exit_json(changed=True, vector_store=current,
                                    diff=dict(before=current, after=changes))
                resp = client.post("vector_stores/{0}".format(current["id"]),
                                   data=changes)
                module.exit_json(changed=True, vector_store=resp)
            else:
                if module.check_mode:
                    module.exit_json(changed=True, vector_store={})
                resp = client.post("vector_stores", data=desired)
                module.exit_json(changed=True, vector_store=resp)
    except OpenAIError as e:
        module.fail_json(msg="Vector store operation failed: {0}".format(str(e)))


if __name__ == "__main__":
    main()
