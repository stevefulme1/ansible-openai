#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: fine_tuning_dataset_validate
short_description: Validate fine-tuning training data
description:
  - Validate fine-tuning training data.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  file_id:
    description: ID of the training file to validate.
    type: str
    required: true
  model:
    description: Target model for validation.
    type: str
    required: false"""

EXAMPLES = r"""
- name: Validate fine-tuning training data
  stevefulme1.openai.fine_tuning_dataset_validate:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
validation:
  description: Validation results.
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
        file_id=dict(type="str", required=True),
        model=dict(type="str", required=False),
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
        payload = {"training_file": module.params["file_id"]}
        if module.params.get("model"):
            payload["model"] = module.params["model"]

        resp = client.post("fine_tuning/jobs", data=payload)
        module.exit_json(changed=True, validation=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"fine_tuning_dataset_validate failed: {str(e)}")


if __name__ == "__main__":
    main()
