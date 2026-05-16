# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment:
    """Documentation fragment for OpenAI modules."""

    DOCUMENTATION = r"""
options:
  api_key:
    description:
      - OpenAI API key for authentication.
      - Can also be set via the C(OPENAI_API_KEY) environment variable.
    type: str
    required: true
  organization:
    description:
      - OpenAI organization ID for API requests.
      - Can also be set via the C(OPENAI_ORGANIZATION) environment variable.
    type: str
    required: false
  base_url:
    description:
      - Base URL for the OpenAI API.
      - Override for Azure OpenAI or compatible endpoints.
      - Defaults to C(https://api.openai.com/v1) when not specified.
    type: str
    required: false
  timeout:
    description:
      - Request timeout in seconds.
    type: int
    required: false
    default: 30
"""
