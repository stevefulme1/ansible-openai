#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: fine_tuning_hyperparameters
short_description: Configure fine-tuning hyperparameters
description:
  - Configure fine-tuning hyperparameters.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: Base model to fine-tune.
    type: str
    required: true
  training_file:
    description: Training file ID.
    type: str
    required: true
  n_epochs:
    description: Number of training epochs.
    type: int
    required: false
  batch_size:
    description: Batch size for training.
    type: int
    required: false
  learning_rate_multiplier:
    description: Learning rate multiplier.
    type: float
    required: false"""

EXAMPLES = r"""
- name: Configure fine-tuning hyperparameters
  stevefulme1.openai.fine_tuning_hyperparameters:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
job:
  description: The fine-tuning job with hyperparameters.
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
        n_epochs=dict(type="int", required=False),
        batch_size=dict(type="int", required=False),
        learning_rate_multiplier=dict(type="float", required=False),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True)

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        hyperparameters = {}
        for opt in ("n_epochs", "batch_size", "learning_rate_multiplier"):
            if module.params.get(opt) is not None:
                hyperparameters[opt] = module.params[opt]
        payload = {
            "model": module.params["model"],
            "training_file": module.params["training_file"],
        }
        if hyperparameters:
            payload["hyperparameters"] = hyperparameters

        resp = client.post("fine_tuning/jobs", data=payload)
        module.exit_json(changed=True, job=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"fine_tuning_hyperparameters failed: {str(e)}")


if __name__ == "__main__":
    main()
