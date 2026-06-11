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
module: fine_tuning_job
short_description: Manage fine-tuning
version_added: "1.0.0"
description:
  - Create, update, and delete fine_tuning_job resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the fine_tuning_job resource.
    type: str
    choices: ['present', 'absent']
    default: present

  model:
    description:
      - >-

    type: str

    required: true

  training_file:
    description:
      - >-
        The ID of an uploaded file that contains training data. See upload...
    type: str

    required: true

  hyperparameters:
    description:
      - >-
        The hyperparameters used for the fine-tuning job. This value is now deprecated in favor of...
    type: dict

  integrations:
    description:
      - >-
        A list of integrations to enable for your fine-tuning job.
    type: list
    elements: dict

  metadata:
    description:
      - >-
        Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
    type: dict

  method:
    description:
      - >-
        The method used for fine-tuning.
    type: dict

  seed:
    description:
      - >-
        The seed controls the reproducibility of the job. Passing in the same seed and job parameters...
    type: int

  suffix:
    description:
      - >-
        A string of up to 64 characters that will be added to your fine-tuned model name. For example, a...
    type: str

    default: null

  validation_file:
    description:
      - >-
        The ID of an uploaded file that contains validation data. If you provide this file, the data is...
    type: str

extends_documentation_fragment:
  - stevefulme1.openai.auth
"""

EXAMPLES = r"""

- name: Create a fine_tuning_job
  stevefulme1.openai.fine_tuning_job:

    model: "example_model"

    training_file: "example_training_file"

    state: present
  # API: POST /fine_tuning/jobs

- name: Update a fine_tuning_job
  stevefulme1.openai.fine_tuning_job:
    id: "existing_id"

    hyperparameters: "updated_hyperparameters"

    integrations: "updated_integrations"

    metadata: "updated_metadata"

    method: "updated_method"

    seed: "updated_seed"

    suffix: "updated_suffix"

    validation_file: "updated_validation_file"

    state: present
  # API:

"""

RETURN = r"""

id:
  description: >-
    The object identifier, which can be referenced in the API endpoints.
  returned: success
  type: str

created_at:
  description: >-
    The Unix timestamp (in seconds) for when the fine-tuning job was created.
  returned: success
  type: int

error:
  description: >-
    For fine-tuning jobs that have failed, this will contain more information on the cause of the failure.
  returned: success
  type: dict

fine_tuned_model:
  description: >-
    The name of the fine-tuned model that is being created. The value will be null if the...
  returned: success
  type: str

finished_at:
  description: >-
    The Unix timestamp (in seconds) for when the fine-tuning job was finished. The value will be...
  returned: success
  type: int

hyperparameters:
  description: >-
    The hyperparameters used for the fine-tuning job. This value will only be returned when running...
  returned: success
  type: dict

model:
  description: >-
    The base model that is being fine-tuned.
  returned: success
  type: str

object:
  description: >-
    The object type, which is always "fine_tuning.job".
  returned: success
  type: str

organization_id:
  description: >-
    The organization that owns the fine-tuning job.
  returned: success
  type: str

result_files:
  description: >-
    The compiled results file ID(s) for the fine-tuning job. You can retrieve the results with the...
  returned: success
  type: list

status:
  description: >-
    The current status of the fine-tuning job, which can be either validating_files, queued,...
  returned: success
  type: str

trained_tokens:
  description: >-
    The total number of billable tokens processed by this fine-tuning job. The value will be null if...
  returned: success
  type: int

training_file:
  description: >-
    The file ID used for training. You can retrieve the training data with the Files...
  returned: success
  type: str

validation_file:
  description: >-
    The file ID used for validation. You can retrieve the validation results with the Files...
  returned: success
  type: str

integrations:
  description: >-
    A list of integrations to enable for this fine-tuning job.
  returned: success
  type: list

seed:
  description: >-
    The seed used for the fine-tuning job.
  returned: success
  type: int

estimated_finish:
  description: >-
    The Unix timestamp (in seconds) for when the fine-tuning job is estimated to finish. The value...
  returned: success
  type: int

method:
  description: >-
    The method used for fine-tuning.
  returned: success
  type: dict

metadata:
  description: >-
    Set of 16 key-value pairs that can be attached to an object. This can be useful for storing...
  returned: success
  type: dict

"""


def get_current_state(client, module):
    """Retrieve the current state of the fine_tuning_job via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    search_key = "id"
    search_value = identifier

    if search_value is None:
        return None
    try:
        items = client.get("/fine_tuning/jobs")
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

    if module.params.get("model") is not None:
        payload["model"] = module.params["model"]

    if module.params.get("training_file") is not None:
        payload["training_file"] = module.params["training_file"]

    if module.params.get("hyperparameters") is not None:
        payload["hyperparameters"] = module.params["hyperparameters"]

    if module.params.get("integrations") is not None:
        payload["integrations"] = module.params["integrations"]

    if module.params.get("metadata") is not None:
        payload["metadata"] = module.params["metadata"]

    if module.params.get("method") is not None:
        payload["method"] = module.params["method"]

    if module.params.get("seed") is not None:
        payload["seed"] = module.params["seed"]

    if module.params.get("suffix") is not None:
        payload["suffix"] = module.params["suffix"]

    if module.params.get("validation_file") is not None:
        payload["validation_file"] = module.params["validation_file"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            model=dict(
                type="str",

                required=True,

            ),

            training_file=dict(
                type="str",

                required=True,

            ),

            hyperparameters=dict(
                type="dict",

            ),

            integrations=dict(
                type="list",
                elements="dict",

            ),

            metadata=dict(
                type="dict",

            ),

            method=dict(
                type="dict",

            ),

            seed=dict(
                type="int",

            ),

            suffix=dict(
                type="str",

                default=None,

            ),

            validation_file=dict(
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
                        "/fine_tuning/jobs",
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
                    path = "/fine_tuning/jobs/{id}".replace(
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

                result["created_at"] = current.get("created_at")

                result["error"] = current.get("error")

                result["fine_tuned_model"] = current.get("fine_tuned_model")

                result["finished_at"] = current.get("finished_at")

                result["hyperparameters"] = current.get("hyperparameters")

                result["model"] = current.get("model")

                result["object"] = current.get("object")

                result["organization_id"] = current.get("organization_id")

                result["result_files"] = current.get("result_files")

                result["status"] = current.get("status")

                result["trained_tokens"] = current.get("trained_tokens")

                result["training_file"] = current.get("training_file")

                result["validation_file"] = current.get("validation_file")

                result["integrations"] = current.get("integrations")

                result["seed"] = current.get("seed")

                result["estimated_finish"] = current.get("estimated_finish")

                result["method"] = current.get("method")

                result["metadata"] = current.get("metadata")

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
