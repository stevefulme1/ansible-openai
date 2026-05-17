#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: usage_info
short_description: Get API usage and cost analytics
description:
  - Retrieves API usage statistics and cost analytics for the organization.
  - Provides aggregated usage data by model, endpoint, and time period.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  start_date:
    description: Start date for the usage period (YYYY-MM-DD).
    type: str
    required: true
  end_date:
    description: End date for the usage period (YYYY-MM-DD).
    type: str
  bucket_width:
    description: Time bucket width for aggregation.
    type: str
    choices: [1m, 1h, 1d]
    default: 1d
  group_by:
    description: Fields to group usage data by.
    type: list
    elements: str
  limit:
    description: Maximum number of results to return.
    type: int
    default: 7
"""

EXAMPLES = r"""
- name: Get usage for the past week
  stevefulme1.openai.usage_info:
    api_key: "{{ openai_api_key }}"
    start_date: "2024-01-01"
  register: result

- name: Get daily usage grouped by model
  stevefulme1.openai.usage_info:
    api_key: "{{ openai_api_key }}"
    start_date: "2024-01-01"
    end_date: "2024-01-31"
    bucket_width: 1d
    group_by:
      - model
  register: result
"""

RETURN = r"""
usage:
  description: Usage data records.
  type: list
  returned: always
  elements: dict
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
        end_date=dict(type="str"),
        bucket_width=dict(type="str", default="1d", choices=["1m", "1h", "1d"]),
        group_by=dict(type="list", elements="str"),
        limit=dict(type="int", default=7),
    )

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

    params = {
        "start_date": module.params["start_date"],
        "bucket_width": module.params["bucket_width"],
        "limit": module.params["limit"],
    }
    if module.params.get("end_date"):
        params["end_date"] = module.params["end_date"]
    if module.params.get("group_by"):
        params["group_by"] = module.params["group_by"]

    try:
        resp = client.get("organization/usage/completions", params=params)
        module.exit_json(changed=False, usage=resp.get("data", []))
    except OpenAIError as e:
        module.fail_json(msg="Failed to get usage info: %s" % str(e))


if __name__ == "__main__":
    main()
