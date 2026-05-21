"""Shared fixtures for stevefulme1.openai unit tests."""
from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import sys
import importlib
import types
from unittest.mock import MagicMock

import pytest

# Build the ansible_collections namespace path so that
# ansible_collections.stevefulme1.openai resolves to the repo root.
COLLECTION_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_fake_root = os.path.join(COLLECTION_ROOT, '.test_namespace')
_ns_path = os.path.join(_fake_root, 'ansible_collections', 'stevefulme1', 'openai')

if not os.path.islink(_ns_path):
    os.makedirs(os.path.join(_fake_root, 'ansible_collections', 'stevefulme1'), exist_ok=True)
    try:
        os.symlink(COLLECTION_ROOT, _ns_path)
    except OSError:
        pass

if _fake_root not in sys.path:
    sys.path.insert(0, _fake_root)

# Ensure the namespace packages are importable
for pkg in ('ansible_collections', 'ansible_collections.stevefulme1'):
    if pkg not in sys.modules:
        try:
            importlib.import_module(pkg)
        except ImportError:
            mod = types.ModuleType(pkg)
            mod.__path__ = [os.path.join(_fake_root, pkg.replace('.', os.sep))]
            mod.__package__ = pkg
            sys.modules[pkg] = mod


@pytest.fixture
def module_args():
    """Return base module args shared by all modules."""
    return {
        "state": "present",
        "api_key": "sk-test-key-12345",
        "organization": None,
        "base_url": "https://api.openai.com/v1",
        "timeout": 30,
    }


@pytest.fixture
def mock_client():
    """Create a mock OpenAI client."""
    client = MagicMock()
    client.get.return_value = None
    client.post.return_value = {"id": "test-123", "object": "test"}
    client.delete.return_value = None
    return client
