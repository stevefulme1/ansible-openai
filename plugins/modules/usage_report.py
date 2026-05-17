#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: usage_report
short_description: Generate usage reports
description:
  - Generate usage reports.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  start_date:
    description: Report start date (YYYY-MM-DD).
    type: str
    required: true
  end_date:
    description: Report end date (YYYY-MM-DD).
    type: str
    required: true
  project_id:
    description: Filter by project.
    type: str
    required: false
"""

EXAMPLES = r"""
- name: Generate usage reports
  stevefulme1.openai.usage_report:
    api_key: "{{ openai_api_key }}"
  register: result
"""

RETURN = r"""
usage:
  description: Usage report data.
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
        start_date=dict(type="str", required=True),
        end_date=dict(type="str", required=True),
        project_id=dict(type="str", required=False),
    )
    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=False)

    client = OpenAIClient(
        api_key=module.params["api_key"],
        organization=module.params["organization"],
        base_url=module.params["base_url"],
        timeout=module.params["timeout"],
    )

    try:
        params = "?start_date={}&end_date={}".format(
            module.params["start_date"],
            module.params["end_date"],
        )
        if module.params.get("project_id"):
            params += "&project_id={}".format(module.params["project_id"])
        endpoint = "organization/usage" + params
        resp = client.get(endpoint)
        module.exit_json(changed=False, usage=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"usage_report failed: {str(e)}")


if __name__ == "__main__":
    main()
