"""
Plugin script for the BEC client. This script is executed after the
IPython shell is started. It is used to load the beamline specific
information and to setup the prompts.

The script is executed in the global namespace of the IPython shell. This
means that all variables defined here are available in the shell.
"""

def extend_command_line_args(parser):
    parser.add_argument("--session", help="Session name", type=str, default="my_default_session")

def setup(parser):
    args = parser.parse_args()

    if args.session == "my_session":
        print("Loading my_session session")
    else:
        print("Loading default session")

    # SETUP PROMPTS
    bec._ip.prompts.username = args.session
    bec._ip.prompts.status = 1

