import builtins
import os
import pathlib
from unittest import mock

from bec_client_lib.user_scripts_mixin import UserScriptsMixin

# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access


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
    builtins.__dict__["dev"] = scripts
    dummy_func.__module__ = "scripts"
    with mock.patch.object(scripts, "_run_linter_on_file") as linter:
        with mock.patch.object(
            scripts,
            "_load_script_module",
            return_value=[("test", dummy_func), ("wrong_test", dummy_func2)],
        ) as load_script:
            scripts.load_user_script("dummy")
            load_script.assert_called_once_with("dummy")
            assert "test" in scripts._scripts
            assert "wrong_test" not in scripts._scripts
        linter.assert_called_once_with("dummy")


def test_user_script_linter():
    scripts = UserScriptsMixin()
    current_path = pathlib.Path(__file__).parent.resolve()
    script_path = os.path.join(current_path, "test_data", "user_script_with_bug.py")
    builtins.__dict__["dev"] = scripts
    with mock.patch("bec_client_lib.user_scripts_mixin.logger") as logger:
        scripts._run_linter_on_file(script_path)
        logger.error.assert_called_once()
