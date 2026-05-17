#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: fine_tuning_wandb_integration
short_description: Configure W&B integration for fine-tuning
description:
  - Configure W&B integration for fine-tuning.
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
  wandb_project:
    description: W&B project name.
    type: str
    required: true
  wandb_api_key:
    description: W&B API key.
    type: str
    required: false"""

EXAMPLES = r"""
- name: Configure W&B integration for fine-tuning
  stevefulme1.openai.fine_tuning_wandb_integration:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
job:
  description: The fine-tuning job with W&B config.
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
        wandb_project=dict(type="str", required=True),
        wandb_api_key=dict(type="str", required=False, no_log=True),
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
        integrations = [
            {
                "type": "wandb",
                "wandb": {
                    "project": module.params["wandb_project"],
                },
            }
        ]
        if module.params.get("wandb_api_key"):
            integrations[0]["wandb"]["api_key"] = module.params["wandb_api_key"]
        payload = {
            "model": module.params["model"],
            "training_file": module.params["training_file"],
            "integrations": integrations,
        }

        resp = client.post("fine_tuning/jobs", data=payload)
        module.exit_json(changed=True, job=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"fine_tuning_wandb_integration failed: {str(e)}")


if __name__ == "__main__":
    main()
