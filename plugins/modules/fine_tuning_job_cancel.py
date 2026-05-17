#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: fine_tuning_job_cancel
short_description: Cancel an OpenAI fine-tuning job
description:
  - Cancels an in-progress fine-tuning job.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  job_id:
    description: ID of the fine-tuning job to cancel.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Cancel a fine-tuning job
  stevefulme1.openai.fine_tuning_job_cancel:
    api_key: "{{ openai_api_key }}"
    job_id: ftjob-abc123
"""

RETURN = r"""
job:
  description: The cancelled fine-tuning job object.
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
    spec["job_id"] = dict(type="str", required=True)

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

    try:
        resp = client.post("fine_tuning/jobs/{}/cancel".format(module.params["job_id"]))
        module.exit_json(changed=True, job=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to cancel fine-tuning job: {str(e)}")


if __name__ == "__main__":
    main()
