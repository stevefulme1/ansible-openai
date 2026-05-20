#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: fine_tuning_job
short_description: Create or monitor an OpenAI fine-tuning job
description:
  - Creates a fine-tuning job to customize a model with training data.
  - Supports state=present (create if not exists) and state=absent (cancel).
  - Idempotent -- looks up existing jobs by suffix+model+training_file.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  state:
    description: Desired state of the fine-tuning job.
    type: str
    choices: [present, absent]
    default: present
  job_id:
    description: ID of an existing fine-tuning job (for cancel or lookup).
    type: str
    required: false
  model:
    description: The base model to fine-tune.
    type: str
    required: false
  training_file:
    description: File ID of the training data.
    type: str
    required: false
  validation_file:
    description: File ID of the validation data.
    type: str
    required: false
  hyperparameters:
    description: Hyperparameters for fine-tuning.
    type: dict
    required: false
  suffix:
    description: Suffix for the fine-tuned model name.
    type: str
    required: false
"""

EXAMPLES = r"""
- name: Create a fine-tuning job
  stevefulme1.openai.fine_tuning_job:
    api_key: "{{ openai_api_key }}"
    model: gpt-3.5-turbo
    training_file: file-abc123
    suffix: my-model
  register: result

- name: Cancel a fine-tuning job
  stevefulme1.openai.fine_tuning_job:
    api_key: "{{ openai_api_key }}"
    job_id: ftjob-abc123
    state: absent
"""

RETURN = r"""
job:
  description: The fine-tuning job object.
  type: dict
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.openai.plugins.module_utils.openai_client import (
    OpenAIClient,
    OpenAIError,
    openai_argument_spec,
)


def get_current_state(client, module):
    """GET the fine-tuning job, return None if not found."""
    job_id = module.params.get("job_id")
    if job_id:
        try:
            return client.get("fine_tuning/jobs/{0}".format(job_id))
        except OpenAIError as e:
            if e.status_code == 404:
                return None
            raise
    # Search for matching active job by model + training_file + suffix
    model = module.params.get("model")
    training_file = module.params.get("training_file")
    suffix = module.params.get("suffix")
    if model and training_file:
        jobs = client.list_paginated("fine_tuning/jobs")
        for job in jobs:
            if job.get("status") in ("succeeded", "failed", "cancelled"):
                continue
            if (job.get("model") == model
                    and job.get("training_file") == training_file
                    and job.get("suffix") == suffix):
                return job
    return None


def needs_update(current, desired):
    """Fine-tuning jobs are immutable once created; no update possible."""
    return {}


def main():
    spec = openai_argument_spec()
    spec.update(
        state=dict(type="str", choices=["present", "absent"], default="present"),
        job_id=dict(type="str", required=False),
        model=dict(type="str", required=False),
        training_file=dict(type="str", required=False),
        validation_file=dict(type="str", required=False),
        hyperparameters=dict(type="dict", required=False),
        suffix=dict(type="str", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("model", "training_file")),
            ("state", "absent", ("job_id",)),
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
                module.exit_json(changed=False, job={})
            if current.get("status") in ("succeeded", "failed", "cancelled"):
                module.exit_json(changed=False, job=current)
            if module.check_mode:
                module.exit_json(changed=True, job=current)
            resp = client.post("fine_tuning/jobs/{0}/cancel".format(current["id"]))
            module.exit_json(changed=True, job=resp)
        else:
            if current:
                module.exit_json(changed=False, job=current)
            if module.check_mode:
                module.exit_json(changed=True, job={})
            payload = dict(
                model=module.params["model"],
                training_file=module.params["training_file"],
            )
            for opt in ("validation_file", "hyperparameters", "suffix"):
                if module.params.get(opt) is not None:
                    payload[opt] = module.params[opt]
            resp = client.post("fine_tuning/jobs", data=payload)
            module.exit_json(changed=True, job=resp)
    except OpenAIError as e:
        module.fail_json(msg="Fine-tuning job operation failed: {0}".format(str(e)))


if __name__ == "__main__":
    main()
