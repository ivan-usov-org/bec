import libtmux


def tmux_launch(bec_path: str, config_path: str, services: dict):
    """
    Launch the BEC server in a tmux session. All services are launched in separate panes.

    Args:
        bec_path (str): Path to the BEC source code
        config (str): Path to the config file
        services (dict): Dictionary of services to launch. Keys are the service names, values are path and command templates.

    """
    tmux_server = libtmux.Server()
    session = tmux_server.new_session(
        "bec", window_name="BEC server. Use `ctrl+b d` to detach.", kill_session=True
    )

    # create panes and run commands
    panes = []
    for ii, service_info in enumerate(services.items()):
        service, service_config = service_info

        if ii == 0:
            pane = session.attached_window.attached_pane
        else:
            pane = session.attached_window.split_window(vertical=False)
        panes.append(pane)
        pane.send_keys(f"cd {service_config['path'].substitute(base_path=bec_path)}")
        pane.send_keys(f"source ./{service}_venv/bin/activate")
        pane.send_keys(service_config["command"].substitute(config_path=config_path))
        session.attached_window.select_layout("tiled")

    session.mouse_all_flag = True
    session.set_option("mouse", "on")


def tmux_stop():
    """
    Stop the BEC server.
    """
    tmux_server = libtmux.Server()
    avail_sessions = tmux_server.sessions.filter(session_name="bec")
    if len(avail_sessions) != 0:
        avail_sessions[0].kill_session()
