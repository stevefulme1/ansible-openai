#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: rate_limit_info
short_description: Get rate limit status
description:
  - Retrieves current rate limit information for the organization.
  - Shows limits and remaining capacity by model and endpoint.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  model:
    description: Filter rate limits to a specific model.
    type: str
"""

EXAMPLES = r"""
- name: Get all rate limits
  stevefulme1.openai.rate_limit_info:
    api_key: "{{ openai_api_key }}"
  register: result

- name: Get rate limits for a specific model
  stevefulme1.openai.rate_limit_info:
    api_key: "{{ openai_api_key }}"
    model: gpt-4
  register: result
"""

RETURN = r"""
rate_limits:
  description: List of rate limit objects.
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
        model=dict(type="str"),
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

    try:
        params = {}
        if module.params.get("model"):
            params["model"] = module.params["model"]
        resp = client.get("organization/rate_limits", params=params)
        module.exit_json(changed=False, rate_limits=resp.get("data", []))
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to get rate limit info: {str(e)}")


if __name__ == "__main__":
    main()
