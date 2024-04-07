from unittest import mock

from bec_server.scan_bundler.cli.launch import main


def test_main():
    with mock.patch("bec_server.scan_bundler.cli.launch.argparse.ArgumentParser") as mock_parser:
        with mock.patch("bec_server.scan_bundler.cli.launch.ServiceConfig") as mock_config:
            with mock.patch("bec_server.scan_bundler.ScanBundler") as mock_scan_bundler:
                with mock.patch("bec_server.scan_bundler.cli.launch.threading.Event") as mock_event:
                    main()
                    mock_parser.assert_called_once()
                    mock_config.assert_called_once()
                    mock_scan_bundler.assert_called_once()
                    mock_event.assert_called_once()


def test_main_shutdown():
    with mock.patch("bec_server.scan_bundler.cli.launch.argparse.ArgumentParser") as mock_parser:
        with mock.patch("bec_server.scan_bundler.cli.launch.ServiceConfig") as mock_config:
            with mock.patch("bec_server.scan_bundler.ScanBundler") as mock_scan_bundler:
                with mock.patch("bec_server.scan_bundler.cli.launch.threading.Event") as mock_event:
                    mock_event.return_value.wait.side_effect = KeyboardInterrupt()
                    try:
                        main()
                    except KeyboardInterrupt:
                        pass
                    mock_parser.assert_called_once()
                    mock_config.assert_called_once()
                    mock_scan_bundler.assert_called_once()
                    mock_event.assert_called_once()
                    mock_scan_bundler.return_value.shutdown.assert_called_once()
