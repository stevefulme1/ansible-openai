#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: fine_tuning_job
short_description: Create an OpenAI fine-tuning job
description:
  - Creates a fine-tuning job to customize a model with training data.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: The base model to fine-tune.
    type: str
    required: true
  training_file:
    description: File ID of the training data.
    type: str
    required: true
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
  register: result
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


def main():
    spec = openai_argument_spec()
    spec.update(
        model=dict(type="str", required=True),
        training_file=dict(type="str", required=True),
        validation_file=dict(type="str", required=False),
        hyperparameters=dict(type="dict", required=False),
        suffix=dict(type="str", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, job={})

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    payload = dict(
        model=module.params["model"],
        training_file=module.params["training_file"],
    )
    for opt in ("validation_file", "hyperparameters", "suffix"):
        if module.params.get(opt) is not None:
            payload[opt] = module.params[opt]

    try:
        resp = client.post("fine_tuning/jobs", data=payload)
        module.exit_json(changed=True, job=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to create fine-tuning job: {str(e)}")


if __name__ == "__main__":
    main()
