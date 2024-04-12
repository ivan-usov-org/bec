"""
Helper script to create a new plugin structure
"""

import os
import sys

# current directory:
current_dir = os.path.dirname(os.path.realpath(__file__))


class PluginStructure:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.create_dir("")

    def create_dir(self, dir_name):
        try:
            os.makedirs(os.path.join(self.target_dir, dir_name))
        except FileExistsError as exc:
            raise FileExistsError(f"Directory {dir_name} already exists") from exc

    def create_init_file(self, dir_name):
        init_file = os.path.join(self.target_dir, dir_name, "__init__.py")
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("")

    def copy_setup_files(self):
        # copy setup files
        setup_file = os.path.join(current_dir, "plugin_setup_files", "setup.py")
        os.system(f"cp {setup_file} {self.target_dir}")
        setup_file = os.path.join(current_dir, "plugin_setup_files", "setup.cfg")
        os.system(f"cp {setup_file} {self.target_dir}")

    def add_plugins(self):
        self.create_dir("bec_plugins")
        self.create_init_file("bec_plugins")

    def add_scan_server(self):
        self.create_dir("bec_plugins/scan_server/scan_plugins")
        self.create_init_file("bec_plugins/scan_server")
        self.create_init_file("bec_plugins/scan_server/scan_plugins")

        # copy scan_plugin_template.py
        scan_plugin_template_file = os.path.join(
            current_dir, "plugin_setup_files", "scan_plugin_template.py"
        )
        os.system(
            f"cp {scan_plugin_template_file} {self.target_dir}/bec_plugins/scan_server/scan_plugins"
        )

    def add_client(self):
        self.create_dir("bec_plugins/bec_ipython_client")
        self.create_init_file("bec_plugins/bec_ipython_client")

        # high level interface
        self.create_dir("bec_plugins/bec_ipython_client/high_level_interface")
        self.create_init_file("bec_plugins/bec_ipython_client/high_level_interface")

        # plugins
        self.create_dir("bec_plugins/bec_ipython_client/plugins")
        self.create_init_file("bec_plugins/bec_ipython_client/plugins")

        # startup
        self.create_dir("bec_plugins/bec_ipython_client/startup")
        self.create_init_file("bec_plugins/bec_ipython_client/startup")
        ## copy pre_startup.py
        pre_startup_file = os.path.join(current_dir, "plugin_setup_files", "pre_startup.py")
        os.system(f"cp {pre_startup_file} {self.target_dir}/bec_plugins/bec_ipython_client/startup")
        ## copy post_startup.py
        post_startup_file = os.path.join(current_dir, "plugin_setup_files", "post_startup.py")
        os.system(
            f"cp {post_startup_file} {self.target_dir}/bec_plugins/bec_ipython_client/startup"
        )

    def add_device_server(self):
        self.create_dir("bec_plugins/device_server")
        self.create_init_file("bec_plugins/device_server")

    def add_devices(self):
        self.create_dir("bec_plugins/devices")
        self.create_init_file("bec_plugins/devices")

    def add_device_configs(self):
        self.create_dir("bec_plugins/device_configs")
        self.create_init_file("bec_plugins/device_configs")

    def add_dap_services(self):
        self.create_dir("bec_plugins/dap_services")
        self.create_init_file("bec_plugins/dap_services")

    def add_bin(self):
        self.create_dir("bin")


if __name__ == "__main__":
    struc = PluginStructure(sys.argv[1])
    struc.add_plugins()
    struc.copy_setup_files()
    struc.add_scan_server()
    struc.add_client()
    struc.add_device_server()
    struc.add_devices()
    struc.add_device_configs()
    struc.add_dap_services()
    struc.add_bin()

    print(f"Plugin structure created in {sys.argv[1]}")
