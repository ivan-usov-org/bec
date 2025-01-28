from unittest.mock import patch

import pytest
from pydantic import ValidationError

from bec_lib import metadata_schema
from bec_lib.messages import ScanQueueMessage
from bec_lib.metadata_schema import BasicScanMetadata

TEST_DICT = {"foo": "bar", "baz": 123}


class ChildMetadata(BasicScanMetadata):
    number_field: int


TEST_REGISTRY = {
    "fake_scan_with_extra_metadata": ChildMetadata,
    "fake_scan_with_basic_metadata": BasicScanMetadata,
}


@pytest.fixture(scope="module", autouse=True)
def clear_schema_registry_cache():
    metadata_schema.cache_clear()


def test_required_fields_validate():
    with pytest.raises(ValidationError):
        test_metadata = ChildMetadata.model_validate(TEST_DICT)

    test_metadata = ChildMetadata.model_validate(TEST_DICT | {"number_field": 123})
    assert test_metadata.number_field == 123
    test_metadata.number_field = 234
    assert test_metadata.number_field == 234

    with pytest.raises(ValidationError):
        test_metadata.number_field = "string"


def test_creating_scan_queue_message_validates_metadata():
    with patch.dict(metadata_schema._METADATA_SCHEMA_REGISTRY, TEST_REGISTRY, clear=True):
        with pytest.raises(ValidationError):
            ScanQueueMessage(scan_type="fake_scan_with_extra_metadata")
        with pytest.raises(ValidationError):
            ScanQueueMessage(
                scan_type="fake_scan_with_extra_metadata",
                parameter={},
                metadata={"number_field", "string"},
            )
        ScanQueueMessage(
            scan_type="fake_scan_with_extra_metadata", parameter={}, metadata={"number_field": 123}
        )
        msg_with_extra_keys = ScanQueueMessage(
            scan_type="fake_scan_with_extra_metadata",
            parameter={},
            metadata={"number_field": 123, "extra": "data"},
        )
        assert msg_with_extra_keys.metadata["extra"] == "data"
