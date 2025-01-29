import importlib
import os
import subprocess
import sys
from time import sleep

import pytest
from pytest import TempPathFactory

from bec_lib import plugin_helper


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def uninstall(package):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package])


class TestPluginSystem:

    @pytest.fixture(scope="class", autouse=True)
    def setup_env(self, tmp_path_factory: TempPathFactory):
        TestPluginSystem._tmp_plugin_dir = tmp_path_factory.mktemp("test_plugin")
        TestPluginSystem._tmp_plugin_name = TestPluginSystem._tmp_plugin_dir.name
        TestPluginSystem._plugin_script = (
            os.path.dirname(os.path.abspath(__file__))
            + "/../util_scripts/create_plugin_structure.py"
        )

        # run plugin generation script
        subprocess.check_call(
            [sys.executable, TestPluginSystem._plugin_script, str(TestPluginSystem._tmp_plugin_dir)]
        )

        # add some test things
        with open(
            TestPluginSystem._tmp_plugin_dir
            / f"{TestPluginSystem._tmp_plugin_name}/scans/__init__.py",
            "w+",
        ) as f:
            f.writelines(
                [
                    "from bec_server.scan_server.scans import ScanBase\n",
                    "class ScanForTesting: ...\n",
                ]
            )

        # install into current environment
        install(TestPluginSystem._tmp_plugin_dir)
        importlib.invalidate_caches()

        yield

        uninstall(TestPluginSystem._tmp_plugin_name)

        TestPluginSystem._tmp_plugin_dir = None

    def test_files_in_plugin_deployment(self, setup_env):
        files = os.listdir(TestPluginSystem._tmp_plugin_dir)
        for file in [
            TestPluginSystem._tmp_plugin_name,
            "pyproject.toml",
            ".git_hooks",
            ".gitignore",
            "LICENSE",
            "tests",
            "bin",
            ".gitlab-ci.yml",
        ]:
            assert file in files

    def test_plugin_module_import_from_file(self, setup_env):
        spec = importlib.util.spec_from_file_location(
            TestPluginSystem._tmp_plugin_name,
            str(TestPluginSystem._tmp_plugin_dir) + "/__init__.py",
        )
        plugin_module = importlib.util.module_from_spec(spec)

    def test_plugin_modules_import_from_file(self, setup_env):
        importlib.import_module(TestPluginSystem._tmp_plugin_name)
        for submod in [
            "scans",
            "devices",
            "bec_widgets",
            "bec_ipython_client",
            "services",
            "file_writer",
        ]:
            importlib.import_module(TestPluginSystem._tmp_plugin_name + "." + submod)

    def test_plugin_helper(self, setup_env):
        scan_plugins = plugin_helper.get_scan_plugins()
        assert "ScanForTesting" in scan_plugins.keys()
