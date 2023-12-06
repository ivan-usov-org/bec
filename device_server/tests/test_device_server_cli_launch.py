from unittest import mock

from device_server.cli.launch import main


def test_main():
    with mock.patch("device_server.cli.launch.argparse.ArgumentParser") as mock_parser:
        with mock.patch("device_server.cli.launch.ServiceConfig") as mock_config:
            mock_config.return_value.redis = "dummy:6379"
            with mock.patch("device_server.DeviceServer") as mock_device_server:
                with mock.patch("device_server.cli.launch.threading.Event") as mock_event:
                    main()
                    mock_parser.assert_called_once()
                    mock_config.assert_called_once()
                    mock_device_server.assert_called_once()
                    mock_event.assert_called_once()


def test_main_shutdown():
    with mock.patch("device_server.cli.launch.argparse.ArgumentParser") as mock_parser:
        with mock.patch("device_server.cli.launch.ServiceConfig") as mock_config:
            mock_config.return_value.redis = "dummy:6379"
            with mock.patch("device_server.DeviceServer") as mock_device_server:
                with mock.patch("device_server.cli.launch.threading.Event") as mock_event:
                    mock_event.return_value.wait.side_effect = KeyboardInterrupt
                    main()
                    mock_parser.assert_called_once()
                    mock_config.assert_called_once()
                    mock_device_server.assert_called_once()
                    mock_event.assert_called_once()
