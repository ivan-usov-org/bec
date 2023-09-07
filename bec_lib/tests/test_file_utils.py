from unittest import mock

import pytest

from bec_lib.core.bec_errors import ServiceConfigError
from bec_lib.core.file_utils import FileWriterMixin


@pytest.mark.parametrize(
    "scan_number,bundle,lead,ref_path",
    [
        (10, 1000, None, "S0000-0999/S0010"),
        (2001, 1000, None, "S2000-2999/S2001"),
        (20, 50, 4, "S0000-0049/S0020"),
        (20, 50, 5, "S00000-00049/S00020"),
        (12000, 100, None, "S12000-12099/S12000"),
        (120, 100, None, "S100-199/S120"),
        (1200, 1000, 5, "S01000-01999/S01200"),
    ],
)
def test_get_scan_dir(scan_number, bundle, lead, ref_path):
    with mock.patch("os.path.expanduser", return_value="/expanded") as mock_expand:
        mixin = FileWriterMixin(service_config={"base_path": "/tmp"})
        dir_path = mixin.get_scan_directory(
            scan_bundle=bundle, scan_number=scan_number, leading_zeros=lead
        )
        assert dir_path == ref_path
        mock_expand.assert_called_once_with("/tmp")


def test_get_base_path_from_config():
    mixin = FileWriterMixin(service_config={"base_path": "/tmp"})
    with mock.patch("os.path.expanduser", return_value="/expanded") as mock_expand:
        base_path = mixin._get_base_path_from_config({"base_path": "/tmp"})
        assert base_path == "/expanded"
        mock_expand.assert_called_once_with("/tmp")


def test_get_base_path_from_config_error():
    with pytest.raises(ServiceConfigError):
        FileWriterMixin({})


def test_get_base_path_from_config_missing_base_path():
    with pytest.raises(Exception):
        FileWriterMixin({"base_path": None})
