# -*- coding: utf-8 -*-
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.stevefulme1.openai.plugins.modules import org_api_key


class TestOrgApiKeyDocumentation:
    def test_documentation_exists(self):
        doc = org_api_key.DOCUMENTATION
        assert "module:" in doc
        assert "short_description:" in doc

    def test_examples_contains_fqcn(self):
        assert "stevefulme1.openai.org_api_key" in org_api_key.EXAMPLES
