# GNU General Public License v3.0+


from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible_collections.stevefulme1.openai.plugins.modules import chat_completion


class TestChatCompletionDocumentation:
    def test_documentation_exists(self):
        doc = chat_completion.DOCUMENTATION
        assert "model" in doc
        assert "messages" in doc

    def test_examples_exists(self):
        assert chat_completion.EXAMPLES is not None
        assert len(chat_completion.EXAMPLES.strip()) > 0
