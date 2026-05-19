#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: realtime_session_config_info
short_description: Get configuration of an OpenAI realtime session
description:
  - Retrieves information about OpenAI session.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  session_id:
    description: ID of the realtime session.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Get configuration of an OpenAI realtime session
  stevefulme1.openai.realtime_session_config_info:
    api_key: "{{ openai_api_key }}"
    session_id: "example_session_id"
  register: result
"""

RETURN = r"""
session:
  description: The session data.
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
    spec["session_id"] = dict(type="str", required=True)

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
        resp = client.get("realtime/sessions/{session_id}".format(session_id=module.params["session_id"]))
        module.exit_json(changed=False, session=resp)
    except OpenAIError as e:
        module.fail_json(msg=f"Failed to retrieve session: {str(e)}")


if __name__ == "__main__":
    main()
