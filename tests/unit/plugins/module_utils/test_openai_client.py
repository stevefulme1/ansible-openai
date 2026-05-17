# GNU General Public License v3.0+


from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible_collections.stevefulme1.openai.plugins.module_utils.openai_client import (
    OpenAIClient,
    OpenAIError,
    openai_argument_spec,
)


class TestOpenAIArgumentSpec:
    def test_has_required_keys(self):
        spec = openai_argument_spec()
        for key in ("api_key", "organization", "base_url", "timeout"):
            assert key in spec, f"Missing key: {key}"

    def test_api_key_no_log(self):
        spec = openai_argument_spec()
        assert spec["api_key"].get("no_log") is True


class TestOpenAIClient:
    def test_init_defaults(self):
        client = OpenAIClient(api_key="sk-test")
        assert client.api_key == "sk-test"
        assert client.organization is None
        assert client.base_url == "https://api.openai.com/v1"
        assert client.timeout == 30

    def test_init_custom(self):
        client = OpenAIClient(
            api_key="sk-test",
            organization="org-123",
            base_url="https://custom.api.com/v1/",
            timeout=60,
        )
        assert client.organization == "org-123"
        assert client.base_url == "https://custom.api.com/v1"
        assert client.timeout == 60


class TestOpenAIError:
    def test_message(self):
        err = OpenAIError("something went wrong", status_code=400)
        assert str(err) == "something went wrong"
        assert err.status_code == 400

    def test_default_attrs(self):
        err = OpenAIError("fail")
        assert err.status_code is None
        assert err.response is None
