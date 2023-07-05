import argparse
import os
from string import Template

from bec_server.tmux_launch import tmux_launch, tmux_stop


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


CONFIG = "../bec_config.yaml"

SERVICES = {
    "scan_server": {
        "path": Template("$base_path/scan_server"),
        "command": Template("bec-scan-server --config $config_path"),
    },
    "scan_bundler": {
        "path": Template("$base_path/scan_bundler"),
        "command": Template("bec-scan-bundler --config $config_path"),
    },
    "device_server": {
        "path": Template("$base_path/device_server"),
        "command": Template("bec-device-server --config $config_path"),
    },
    "file_writer": {
        "path": Template("$base_path/file_writer"),
        "command": Template("bec-file-writer --config $config_path"),
    },
    "scihub": {
        "path": Template("$base_path/scihub"),
        "command": Template("bec-scihub --config $config_path"),
    },
    "data_processing": {
        "path": Template("$base_path/data_processing"),
        "command": Template("bec-dap --config $config_path"),
    },
}


def main():
    """
    Launch the BEC server in a tmux session. All services are launched in separate panes.
    """
    parser = argparse.ArgumentParser(description="Utility tool managing the BEC server")
    parser.add_argument(
        "--start",
        action="store_true",
        help="Start the BEC server",
    )
    parser.add_argument(
        "--stop",
        action="store_true",
        help="Stop the BEC server",
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Restart the BEC server",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Get the status of the BEC server",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="bec_config.yaml",
        help="Path to the config file",
    )

    args = parser.parse_args()
    if args.start:
        print("Starting BEC server using tmux...")
        bec_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        tmux_launch(bec_path, CONFIG, SERVICES)
        print(
            f"{bcolors.OKCYAN}{bcolors.BOLD}Use `tmux attach -t bec` to attach to the BEC server. Once connected, use `ctrl+b d` to detach again."
        )
    elif args.stop:
        print("Stopping BEC server...")
        tmux_stop()
    elif args.restart:
        print("Restarting BEC server...")
        tmux_stop()
        bec_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        tmux_launch(bec_path, CONFIG, SERVICES)
        print(
            f"{bcolors.OKCYAN}{bcolors.BOLD}Use `tmux attach -t bec` to attach to the BEC server. Once connected, use `ctrl+b d` to detach again."
        )
