import asyncio
from unittest import mock
from bec_lib import messages

import pytest

from bec_client.callbacks.scan_progress import LiveUpdatesScanProgress
from bec_lib import MessageEndpoints


@pytest.mark.asyncio
async def test_update_progressbar_continues_without_device_data():
    bec = mock.MagicMock()
    request = mock.MagicMock()
    live_update = LiveUpdatesScanProgress(bec=bec, report_instruction={}, request=request)
    progressbar = mock.MagicMock()

    bec.producer.get.return_value = None
    res = await live_update._update_progressbar(progressbar, "async_dev1")
    assert res is False


@pytest.mark.asyncio
async def test_update_progressbar_continues_when_scanID_doesnt_match():
    bec = mock.MagicMock()
    request = mock.MagicMock()
    live_update = LiveUpdatesScanProgress(bec=bec, report_instruction={}, request=request)
    progressbar = mock.MagicMock()
    live_update.scan_item = mock.MagicMock()
    live_update.scan_item.scanID = "scanID2"

    bec.producer.get.return_value = messages.ProgressMessage(
        value=1, max_value=10, done=False, metadata={"scanID": "scanID"}
    )
    res = await live_update._update_progressbar(progressbar, "async_dev1")
    assert res is False


@pytest.mark.asyncio
async def test_update_progressbar_continues_when_msg_specifies_no_value():
    bec = mock.MagicMock()
    request = mock.MagicMock()
    live_update = LiveUpdatesScanProgress(bec=bec, report_instruction={}, request=request)
    progressbar = mock.MagicMock()
    live_update.scan_item = mock.MagicMock()
    live_update.scan_item.scanID = "scanID"

    bec.producer.get.return_value = messages.ProgressMessage(
        value=None, max_value=None, done=None, metadata={"scanID": "scanID"}
    )
    res = await live_update._update_progressbar(progressbar, "async_dev1")
    assert res is False


@pytest.mark.asyncio
async def test_update_progressbar_updates_max_value():
    bec = mock.MagicMock()
    request = mock.MagicMock()
    live_update = LiveUpdatesScanProgress(bec=bec, report_instruction={}, request=request)
    progressbar = mock.MagicMock()
    live_update.scan_item = mock.MagicMock()
    live_update.scan_item.scanID = "scanID"

    bec.producer.get.return_value = messages.ProgressMessage(
        value=10, max_value=20, done=False, metadata={"scanID": "scanID"}
    )
    res = await live_update._update_progressbar(progressbar, "async_dev1")
    assert res is False
    assert progressbar.max_points == 20
    progressbar.update.assert_called_once_with(10)


@pytest.mark.asyncio
async def test_update_progressbar_returns_true_when_max_value_is_reached():
    bec = mock.MagicMock()
    request = mock.MagicMock()
    live_update = LiveUpdatesScanProgress(bec=bec, report_instruction={}, request=request)
    progressbar = mock.MagicMock()
    live_update.scan_item = mock.MagicMock()
    live_update.scan_item.scanID = "scanID"

    bec.producer.get.return_value = messages.ProgressMessage(
        value=10, max_value=10, done=True, metadata={"scanID": "scanID"}
    )
    res = await live_update._update_progressbar(progressbar, "async_dev1")
    assert res is True
