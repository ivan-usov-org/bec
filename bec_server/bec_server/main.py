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


SERVICES = {
    "scan_server": {
        "path": Template("$base_path/scan_server"),
        "command": "bec-scan-server",
    },
    "scan_bundler": {"path": Template("$base_path/scan_bundler"), "command": "bec-scan-bundler"},
    "device_server": {"path": Template("$base_path/device_server"), "command": "bec-device-server"},
    "file_writer": {"path": Template("$base_path/file_writer"), "command": "bec-file-writer"},
    "scihub": {"path": Template("$base_path/scihub"), "command": "bec-scihub"},
    "data_processing": {"path": Template("$base_path/data_processing"), "command": "bec-dap"},
}


def main():
    """
    Launch the BEC server in a tmux session. All services are launched in separate panes.
    """
    parser = argparse.ArgumentParser(description="Utility tool managing the BEC server")
    command = parser.add_subparsers(dest="command")
    command.add_parser("start", help="Start the BEC server")
    command.add_parser("stop", help="Stop the BEC server")
    command.add_parser("restart", help="Restart the BEC server")
    command.add_parser("status", help="Show the status of the BEC server")

    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to the BEC service config file",
    )

    args = parser.parse_args()
    if args.command == "start":
        print("Starting BEC server using tmux...")
        bec_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        tmux_launch(bec_path, args.config, SERVICES)
        print(
            f"{bcolors.OKCYAN}{bcolors.BOLD}Use `tmux attach -t bec` to attach to the BEC server. Once connected, use `ctrl+b d` to detach again."
        )
    elif args.command == "stop":
        print("Stopping BEC server...")
        tmux_stop()
    elif args.command == "restart":
        print("Restarting BEC server...")
        tmux_stop()
        bec_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        tmux_launch(bec_path, args.config, SERVICES)
        print(
            f"{bcolors.OKCYAN}{bcolors.BOLD}Use `tmux attach -t bec` to attach to the BEC server. Once connected, use `ctrl+b d` to detach again."
        )
