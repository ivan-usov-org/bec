import builtins
from unittest import mock

from bec_client.user_scripts_mixin import UserScriptsMixin


def dummy_func():
    pass


def dummy_func2():
    pass


def test_user_scripts_forget():
    scripts = UserScriptsMixin()
    scripts._scripts = {"test": {"cls": dummy_func, "file": "path_to_my_file.py"}}
    builtins.test = dummy_func
    scripts.forget_all_user_scripts()
    assert "test" not in builtins.__dict__
    assert len(scripts._scripts) == 0


def test_user_script_forget():
    scripts = UserScriptsMixin()
    scripts._scripts = {"test": {"cls": dummy_func, "file": "path_to_my_file.py"}}
    builtins.test = dummy_func
    scripts.forget_user_script("test")
    assert "test" not in builtins.__dict__


def test_load_user_script():
    scripts = UserScriptsMixin()
    dummy_func.__module__ = "scripts"
    with mock.patch.object(
        scripts,
        "_load_script_module",
        return_value=[("test", dummy_func), ("wrong_test", dummy_func2)],
    ) as load_script:
        scripts.load_user_script("dummy")
        load_script.assert_called_once_with("dummy")
        assert "test" in scripts._scripts
        assert "wrong_test" not in scripts._scripts
