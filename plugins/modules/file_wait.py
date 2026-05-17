#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: file_wait
short_description: Wait for file processing to complete
description:
  - Polls file status until processing completes.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  file_id:
    description: ID of the file to wait for.
    type: str
    required: true
  poll_interval:
    description: Seconds between status checks.
    type: int
    default: 5
  max_wait:
    description: Maximum seconds to wait.
    type: int
    default: 300
"""

EXAMPLES = r"""
- name: Wait for file processing
  stevefulme1.openai.file_wait:
    api_key: "{{ openai_api_key }}"
    file_id: file-abc123
  register: result
"""

RETURN = r"""
file:
  description: The file object once processing completes.
  type: dict
  returned: always
"""

import time

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
        poll_interval=dict(type="int", default=5),
        max_wait=dict(type="int", default=300),
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

    fid = module.params["file_id"]
    interval = module.params["poll_interval"]
    max_wait = module.params["max_wait"]
    elapsed = 0

    try:
        while elapsed < max_wait:
            resp = client.get(f"files/{fid}")
            status = resp.get("status", "")
            if status == "processed":
                module.exit_json(changed=False, file=resp)
            if status == "error":
                module.fail_json(msg=f"File processing failed: {resp}")
            time.sleep(interval)
            elapsed += interval
        module.fail_json(msg=f"Timed out waiting for file {fid}")
    except OpenAIError as e:
        module.fail_json(msg=f"file_wait failed: {str(e)}")


if __name__ == "__main__":
    main()
