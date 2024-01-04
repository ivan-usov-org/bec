from os import path

import IPython
import pkg_resources
from traitlets.config import Config


def main():
    """Launch BEC IPython client"""
    c = Config()
    startup_file = path.join(path.dirname(path.abspath(__file__)), "bec_startup.py")
    c.TerminalIPythonApp.exec_files = [startup_file]
    c.TerminalIPythonApp.force_interact = True
    version = pkg_resources.get_distribution("bec-ipython-client").version
    c.TerminalInteractiveShell.banner2 = f"BEC IPython client: {version}\n\n"

    IPython.start_ipython(config=c)


if __name__ == "__main__":
    main()
