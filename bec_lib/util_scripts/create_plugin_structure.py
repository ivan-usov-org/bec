"""
Helper script to create a new plugin structure
"""

import os
import sys

# current directory:
current_dir = os.path.dirname(os.path.realpath(__file__))


class PluginStructure:
    """
    Example usage. Run this script with the target directory as an argument
    It will then automatically create the plugin structure in the target directory

    >>> python create_plugin_structure.py /path/to/my_plugin
    """

    def __init__(self, target_dir):
        """This class can be used to produce the folder structure
        of BEC. This includes copying templates for the structures
        """
        self.target_dir = target_dir
        _, self.plugin_name = os.path.split(target_dir)
        self.create_dir("")

    def create_dir(self, dir_name):
        os.makedirs(os.path.join(self.target_dir, dir_name), exist_ok=True)

    def create_init_file(self, dir_name):
        init_file = os.path.join(self.target_dir, dir_name, "__init__.py")
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("")

    def copy_plugin_setup_files(self):
        # copy setup files
        self.copy_toml_file()
        git_hooks = os.path.join(current_dir, "plugin_setup_files", ".git_hooks")
        os.system(f"cp -R {git_hooks} {self.target_dir}")
        gitignore = os.path.join(current_dir, "plugin_setup_files", ".gitignore")
        os.system(f"cp {gitignore} {self.target_dir}")

    def copy_toml_file(self):
        """Copy the toml file and change the template name in the file"""
        # copy toml file
        toml_file = os.path.join(current_dir, "plugin_setup_files", "pyproject.toml")
        with open(toml_file, "r", encoding="utf-8") as f:
            toml_template_str = f.read()
        # change template name in toml file
        toml_template_str = toml_template_str.replace("{template_name}", self.plugin_name)

        toml_file = os.path.join(self.target_dir, "pyproject.toml")
        # write toml file
        with open(toml_file, "w", encoding="utf-8") as f:
            f.write(toml_template_str)

    def add_plugins(self):
        self.create_dir(self.plugin_name)
        self.create_init_file(self.plugin_name)

    def add_scans(self):
        self.create_dir(f"{self.plugin_name}/scans")
        self.create_init_file(f"{self.plugin_name}/scans")

        # copy scan_plugin_template.py
        scan_plugin_template_file = os.path.join(
            current_dir, "plugin_setup_files", "scan_plugin_template.py"
        )
        os.system(f"cp {scan_plugin_template_file} {self.target_dir}/{self.plugin_name}/scans")

    def add_client(self):
        self.create_dir(f"{self.plugin_name}/bec_ipython_client")
        self.create_init_file(f"{self.plugin_name}/bec_ipython_client")

        # high level interface
        self.create_dir(f"{self.plugin_name}/bec_ipython_client/high_level_interface")
        self.create_init_file(f"{self.plugin_name}/bec_ipython_client/high_level_interface")

        # plugins
        self.create_dir(f"{self.plugin_name}/bec_ipython_client/plugins")
        self.create_init_file(f"{self.plugin_name}/bec_ipython_client/plugins")

        # startup
        self.create_dir(f"{self.plugin_name}/bec_ipython_client/startup")
        self.create_init_file(f"{self.plugin_name}/bec_ipython_client/startup")

        ## copy pre_startup.py
        pre_startup_file = os.path.join(current_dir, "plugin_setup_files", "pre_startup.py")
        os.system(
            f"cp {pre_startup_file} {self.target_dir}/{self.plugin_name}/bec_ipython_client/startup"
        )
        ## copy post_startup.py
        post_startup_file = os.path.join(current_dir, "plugin_setup_files", "post_startup.py")
        os.system(
            f"cp {post_startup_file} {self.target_dir}/{self.plugin_name}/bec_ipython_client/startup"
        )

    def add_devices(self):
        self.create_dir(f"{self.plugin_name}/devices")
        self.create_init_file(f"{self.plugin_name}/devices")
        # device template?

    def add_device_configs(self):
        self.create_dir(f"{self.plugin_name}/device_configs")
        self.create_init_file(f"{self.plugin_name}/device_configs")

    def add_dap_services(self):
        self.create_dir(f"{self.plugin_name}/dap_services")
        self.create_init_file(f"{self.plugin_name}/dap_services")

    def add_bec_widgets(self):
        self.create_dir(f"{self.plugin_name}/bec_widgets")
        self.create_init_file(f"{self.plugin_name}/bec_widgets")

    def add_tests(self):
        self.create_dir("tests/tests_bec_ipython_client")
        self.create_dir("tests/tests_dap_services")
        self.create_dir("tests/tests_bec_widgets")
        self.create_dir("tests/tests_devices")
        self.create_dir("tests/tests_scans")

    def add_bin(self):
        self.create_dir("bin")


if __name__ == "__main__":
    struc = PluginStructure(sys.argv[1])
    struc.add_plugins()
    struc.copy_plugin_setup_files()
    struc.add_scans()
    struc.add_client()
    struc.add_devices()
    struc.add_device_configs()
    struc.add_dap_services()
    struc.add_bec_widgets()
    struc.add_tests()
    struc.add_bin()

    print(f"Plugin structure created in {sys.argv[1]}")
