#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = r"""
---
module: fine_tuning_job_detail_info
short_description: Get details of a specific fine-tuning job
description:
  - Retrieves detailed information about a fine-tuning job.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  job_id:
    description: ID of the fine-tuning job.
    type: str
    required: true
  limit:
    description:
      - Maximum number of results to return.
    type: int
    default: 100
  offset:
    description:
      - Number of results to skip for pagination.
    type: int
    default: 0
"""

EXAMPLES = r"""
- name: Get fine-tuning job details
  stevefulme1.openai.fine_tuning_job_detail_info:
    api_key: "{{ openai_api_key }}"
    job_id: ftjob-abc123
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
    spec["job_id"] = dict(type="str", required=True)
    spec["limit"] = dict(type="int", required=False, default=100)
    spec["offset"] = dict(type="int", required=False, default=0)

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        resp = client.get("fine_tuning/jobs/{}".format(module.params["job_id"]))
        module.exit_json(changed=False, job=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to get fine-tuning job: {str(e)}")


if __name__ == "__main__":
    main()
