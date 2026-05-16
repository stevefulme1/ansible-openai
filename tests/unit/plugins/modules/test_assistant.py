# -*- coding: utf-8 -*-
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.stevefulme1.openai.plugins.modules import assistant


class TestAssistantDocumentation:
    def test_documentation_has_required_fields(self):
        doc = assistant.DOCUMENTATION
        assert "module:" in doc
        assert "short_description:" in doc
        assert "description:" in doc
        assert "options:" in doc

    def test_examples_contains_fqcn(self):
        assert "stevefulme1.openai.assistant" in assistant.EXAMPLES

    def test_return_exists(self):
        assert assistant.RETURN is not None
        assert len(assistant.RETURN.strip()) > 0
