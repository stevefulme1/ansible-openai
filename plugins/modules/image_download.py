#!/usr/bin/python
# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: image_download
short_description: Download generated images to local path
description:
  - Downloads an image from a URL to a local file path.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.openai.openai
options:
  url:
    description: URL of the image to download.
    type: str
    required: true
  dest:
    description: Local file path to save the image.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Download a generated image
  stevefulme1.openai.image_download:
    api_key: "{{ openai_api_key }}"
    url: "https://oaidalleapiprodscus.blob.core.windows.net/..."
    dest: /tmp/image.png
  register: result
"""

RETURN = r"""
path:
  description: Local path where the image was saved.
  type: str
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url
from ansible_collections.stevefulme1.openai.plugins.module_utils.openai_client import (
    openai_argument_spec,
)


def main():
    spec = openai_argument_spec()
    spec.update(
        url=dict(type="str", required=True),
        dest=dict(type="str", required=True),
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        resp = open_url(module.params["url"])
        with open(module.params["dest"], "wb") as f:
            f.write(resp.read())
        module.exit_json(changed=True, path=module.params["dest"])
    except Exception as e:
        module.fail_json(msg=f"image_download failed: {str(e)}")


if __name__ == "__main__":
    main()
