import os

import pytest


@pytest.fixture()
def set_env():
    """Factory fixture that allows to add env variables.

    Environment variables created with this fixture only exist within the test.

    Examples:
        def test_foo(set_env):
            set_env(a="34", b="Hello World")
            import os
            assert os.environ.get("a") == "34"
    """
    added_env = []

    def _wrapped(**kwargs):
        added_env.extend(kwargs.keys())
        os.environ.update(kwargs)

    yield _wrapped

    for key in added_env:
        os.environ.pop(key)
