from unittest import mock

from bec_server.file_writer.cli.launch import main


def test_main():
    with mock.patch("bec_server.file_writer.cli.launch.argparse.ArgumentParser") as mock_parser:
        with mock.patch("bec_server.file_writer.cli.launch.ServiceConfig") as mock_config:
            with mock.patch("bec_server.file_writer.FileWriterManager") as mock_file_writer:
                with mock.patch("bec_server.file_writer.cli.launch.threading.Event") as mock_event:
                    main()
                    mock_parser.assert_called_once()
                    mock_config.assert_called_once()
                    mock_file_writer.assert_called_once()
                    mock_event.assert_called_once()


def test_main_shutdown():
    with mock.patch("bec_server.file_writer.cli.launch.argparse.ArgumentParser") as mock_parser:
        with mock.patch("bec_server.file_writer.cli.launch.ServiceConfig") as mock_config:
            with mock.patch("bec_server.file_writer.FileWriterManager") as mock_file_writer:
                with mock.patch("bec_server.file_writer.cli.launch.threading.Event") as mock_event:
                    mock_event.return_value.wait.side_effect = KeyboardInterrupt()
                    try:
                        main()
                    except KeyboardInterrupt:
                        pass
                    mock_parser.assert_called_once()
                    mock_config.assert_called_once()
                    mock_file_writer.assert_called_once()
                    mock_event.assert_called_once()
                    mock_file_writer.return_value.shutdown.assert_called_once()
