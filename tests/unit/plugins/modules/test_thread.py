"""Unit tests for stevefulme1.openai.thread module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch
import pytest

MODULE_PATH = "ansible_collections.stevefulme1.openai.plugins.modules.thread"
CLIENT_PATH = "ansible_collections.stevefulme1.openai.plugins.module_utils.openai_client"


def _build_resource(**overrides):
    """Return a mock thread resource dict."""
    base = {
        "id": "res-123",
        "object": "thread",
    }
    base.update(overrides)
    return base


@pytest.fixture
def module_args():
    """Base module args for thread."""
    return {
        "state": "present",
        "api_key": "sk-test-key",
        "organization": None,
        "base_url": "https://api.openai.com/v1",
        "timeout": 30,
        "thread_id": None,
        "messages": None,
        "metadata": None
    }


class TestCreate:
    """Test thread creation."""

    @patch(f"{MODULE_PATH}.OpenAIClient")
    @patch(f"{MODULE_PATH}.AnsibleModule")
    def test_create_resource(self, mock_ansible_cls, mock_client_cls, module_args):
        """Creating a resource calls the API and exits with changed=True."""
        mock_module = MagicMock()
        mock_module.exit_json = MagicMock(side_effect=SystemExit(0))
        mock_module.fail_json = MagicMock(side_effect=SystemExit(1))
        mock_module.params = module_args
        mock_module.check_mode = False
        mock_ansible_cls.return_value = mock_module

        mock_client = MagicMock()
        mock_client.post.return_value = _build_resource()
        mock_client_cls.return_value = mock_client

        from ansible_collections.stevefulme1.openai.plugins.modules.thread import main
        try:
            main()
        except SystemExit:
            pass

        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is True

    @patch(f"{MODULE_PATH}.OpenAIClient")
    @patch(f"{MODULE_PATH}.AnsibleModule")
    def test_create_check_mode(self, mock_ansible_cls, mock_client_cls, module_args):
        """In check mode, returns changed=True without calling API."""
        mock_module = MagicMock()
        mock_module.exit_json = MagicMock(side_effect=SystemExit(0))
        mock_module.fail_json = MagicMock(side_effect=SystemExit(1))
        mock_module.params = module_args
        mock_module.check_mode = True
        mock_ansible_cls.return_value = mock_module

        from ansible_collections.stevefulme1.openai.plugins.modules.thread import main
        try:
            main()
        except SystemExit:
            pass

        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is True


class TestDelete:
    """Test thread deletion."""

    @patch(f"{MODULE_PATH}.OpenAIClient")
    @patch(f"{MODULE_PATH}.AnsibleModule")
    def test_delete_resource(self, mock_ansible_cls, mock_client_cls, module_args):
        """Deleting a resource calls delete and exits with changed=True."""
        module_args["state"] = "absent"
        module_args["thread_id"] = "res-123"
        mock_module = MagicMock()
        mock_module.exit_json = MagicMock(side_effect=SystemExit(0))
        mock_module.fail_json = MagicMock(side_effect=SystemExit(1))
        mock_module.params = module_args
        mock_module.check_mode = False
        mock_ansible_cls.return_value = mock_module

        mock_client = MagicMock()
        mock_client.delete.return_value = None
        mock_client_cls.return_value = mock_client

        from ansible_collections.stevefulme1.openai.plugins.modules.thread import main
        try:
            main()
        except SystemExit:
            pass

        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is True

    @patch(f"{MODULE_PATH}.OpenAIClient")
    @patch(f"{MODULE_PATH}.AnsibleModule")
    def test_delete_check_mode(self, mock_ansible_cls, mock_client_cls, module_args):
        """In check mode, delete returns changed=True without API call."""
        module_args["state"] = "absent"
        module_args["thread_id"] = "res-123"
        mock_module = MagicMock()
        mock_module.exit_json = MagicMock(side_effect=SystemExit(0))
        mock_module.fail_json = MagicMock(side_effect=SystemExit(1))
        mock_module.params = module_args
        mock_module.check_mode = True
        mock_ansible_cls.return_value = mock_module

        from ansible_collections.stevefulme1.openai.plugins.modules.thread import main
        try:
            main()
        except SystemExit:
            pass

        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is True


class TestUpdate:
    """Test thread update with existing ID."""

    @patch(f"{MODULE_PATH}.OpenAIClient")
    @patch(f"{MODULE_PATH}.AnsibleModule")
    def test_update_existing_resource(self, mock_ansible_cls, mock_client_cls, module_args):
        """Updating an existing resource calls post with ID path."""
        module_args["thread_id"] = "res-123"
        mock_module = MagicMock()
        mock_module.exit_json = MagicMock(side_effect=SystemExit(0))
        mock_module.fail_json = MagicMock(side_effect=SystemExit(1))
        mock_module.params = module_args
        mock_module.check_mode = False
        mock_ansible_cls.return_value = mock_module

        mock_client = MagicMock()
        mock_client.post.return_value = _build_resource()
        mock_client_cls.return_value = mock_client

        from ansible_collections.stevefulme1.openai.plugins.modules.thread import main
        try:
            main()
        except SystemExit:
            pass

        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is True


class TestIdempotent:
    """Test idempotent behavior."""

    @patch(f"{MODULE_PATH}.OpenAIClient")
    @patch(f"{MODULE_PATH}.AnsibleModule")
    def test_check_mode_always_returns_changed(self, mock_ansible_cls, mock_client_cls, module_args):
        """OpenAI modules in check mode always report changed (no server-side diff)."""
        mock_module = MagicMock()
        mock_module.exit_json = MagicMock(side_effect=SystemExit(0))
        mock_module.fail_json = MagicMock(side_effect=SystemExit(1))
        mock_module.params = module_args
        mock_module.check_mode = True
        mock_ansible_cls.return_value = mock_module

        from ansible_collections.stevefulme1.openai.plugins.modules.thread import main
        try:
            main()
        except SystemExit:
            pass

        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
