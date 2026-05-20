#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: file
short_description: Manage files
version_added: "1.0.0"
description:
  - Create, update, and delete file resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Auto-generated"
options:
  state:
    description:
      - Desired state of the file resource.
    type: str
    choices: ['present', 'absent']
    default: present

  file:
    description:
      - >-
        The File object (not file name) to be uploaded.
    type: str

    required: true





  purpose:
    description:
      - >-
        The intended purpose of the uploaded file. One of: - assistants: Used in the Assistants API -...
    type: str

    required: true


    choices: ["assistants", "batch", "fine-tune", "vision", "user_data", "evals"]




  expires_after:
    description:
      - >-
        The expiration policy for a file. By default, files with purpose=batch expire after 30 days and...
    type: dict





extends_documentation_fragment:
  - stevefulme1.openai.auth
"""

EXAMPLES = r"""

- name: Create a file
  stevefulme1.openai.file:


    file: "example_file"



    purpose: "example_purpose"




    state: present
  # API: POST /files



- name: Update a file
  stevefulme1.openai.file:
    id: "existing_id"






    expires_after: "updated_expires_after"


    state: present
  # API:  



- name: Delete a file
  stevefulme1.openai.file:
    id: "existing_id"
    state: absent
  # API: DELETE /files/{file_id}

"""

RETURN = r"""

id:
  description: >-
    The file identifier, which can be referenced in the API endpoints.
  returned: success
  type: str


bytes:
  description: >-
    The size of the file, in bytes.
  returned: success
  type: int


created_at:
  description: >-
    The Unix timestamp (in seconds) for when the file was created.
  returned: success
  type: int


expires_at:
  description: >-
    The Unix timestamp (in seconds) for when the file will expire.
  returned: success
  type: int


filename:
  description: >-
    The name of the file.
  returned: success
  type: str


object:
  description: >-
    The object type, which is always file.
  returned: success
  type: str


purpose:
  description: >-
    The intended purpose of the file. Supported values are assistants, assistants_output, batch,...
  returned: success
  type: str


status:
  description: >-
    Deprecated. The current status of the file, which can be either uploaded, processed, or error.
  returned: success
  type: str


status_details:
  description: >-
    Deprecated. For details on why a fine-tuning training file failed validation, see the error...
  returned: success
  type: str


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.openai.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the file via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    search_key = "id"
    search_value = identifier

    if search_value is None:
        return None
    try:
        items = client.get("/files")
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

    if module.params.get("file") is not None:
        payload["file"] = module.params["file"]

    if module.params.get("purpose") is not None:
        payload["purpose"] = module.params["purpose"]

    if module.params.get("expires_after") is not None:
        payload["expires_after"] = module.params["expires_after"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            file=dict(
                type="str",

                required=True,





            ),

            purpose=dict(
                type="str",

                required=True,


                choices=['assistants', 'batch', 'fine-tune', 'vision', 'user_data', 'evals'],




            ),

            expires_after=dict(
                type="dict",





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
                        "/files",
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
                    path = "".replace(
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

                result["bytes"] = current.get("bytes")

                result["created_at"] = current.get("created_at")

                result["expires_at"] = current.get("expires_at")

                result["filename"] = current.get("filename")

                result["object"] = current.get("object")

                result["purpose"] = current.get("purpose")

                result["status"] = current.get("status")

                result["status_details"] = current.get("status_details")


        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/files/{file_id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
