import _thread
import threading
import time

import numpy as np
import pytest
from bec_client import BKClient
from bec_client.alarm_handler import AlarmBase
from bec_utils import RedisConnector, ServiceConfig, bec_logger
from bec_utils.bec_errors import ScanInterruption

CONFIG_PATH = "../test_config.yaml"

# pylint: disable=no-member


@pytest.mark.timeout(200)
def start_client():
    config = ServiceConfig(CONFIG_PATH)
    bec = BKClient(
        [config.redis],
        RedisConnector,
        config.scibec,
    )
    bec.start()
    return bec


@pytest.mark.timeout(200)
def test_grid_scan(capsys):
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    status = scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.01)
    assert len(status.scan.data) == 100
    assert status.scan.num_points == 100
    captured = capsys.readouterr()
    assert "finished. Scan ID" in captured.out


@pytest.mark.timeout(200)
def test_fermat_scan(capsys):
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    status = scans.fermat_scan(dev.samx, -5, 5, dev.samy, -5, 5, step=0.5, exp_time=0.01)
    assert len(status.scan.data) == 199
    assert status.scan.num_points == 199
    captured = capsys.readouterr()
    assert "finished. Scan ID" in captured.out


@pytest.mark.timeout(200)
def test_line_scan(capsys):
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    status = scans.line_scan(dev.samx, -5, 5, steps=10, exp_time=0.01)
    assert len(status.scan.data) == 10
    assert status.scan.num_points == 10
    captured = capsys.readouterr()
    assert "finished. Scan ID" in captured.out


@pytest.mark.timeout(200)
def test_mv_scan(capsys):
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    scans.umv(dev.samx, 10, dev.samy, 20)
    current_pos_samx = dev.samx.read()["samx"]["value"]
    current_pos_samy = dev.samy.read()["samy"]["value"]
    assert np.isclose(
        current_pos_samx, 10, atol=dev.samx.config["deviceConfig"].get("tolerance", 0.05)
    )
    assert np.isclose(
        current_pos_samy, 20, atol=dev.samy.config["deviceConfig"].get("tolerance", 0.05)
    )
    scans.umv(dev.samx, 10, dev.samy, 20)
    current_pos_samx = dev.samx.read()["samx"]["value"]
    current_pos_samy = dev.samy.read()["samy"]["value"]
    captured = capsys.readouterr()
    ref_out_samx = f" ━━━━━━━━━━━━━━━ {current_pos_samx:10.2f} /      10.00 / 100 % 0:00:00 0:00:00"
    ref_out_samy = f" ━━━━━━━━━━━━━━━ {current_pos_samy:10.2f} /      20.00 / 100 % 0:00:00 0:00:00"
    assert ref_out_samx in captured.out
    assert ref_out_samy in captured.out


@pytest.mark.timeout(200)
def test_mv_scan_mv():
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    scans.umv(dev.samx, 10, dev.samy, 20)
    tolerance_samx = dev.samx.config["deviceConfig"].get("tolerance", 0.05)
    tolerance_samy = dev.samy.config["deviceConfig"].get("tolerance", 0.05)
    current_pos_samx = dev.samx.read()["samx"]["value"]
    current_pos_samy = dev.samy.read()["samy"]["value"]

    # make sure the current position after mv is within the tolerance
    assert np.isclose(current_pos_samx, 10, atol=tolerance_samx)
    assert np.isclose(current_pos_samy, 20, atol=tolerance_samy)

    status = scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.01)

    # make sure the scan completed the expected number of positions
    assert len(status.scan.data) == 100
    assert status.scan.num_points == 100

    # make sure the scan is relative to the starting position
    assert np.isclose(
        current_pos_samx - 5,
        status.scan.data[0].content["data"]["samx"]["samx"]["value"],
        atol=tolerance_samx,
    )

    current_pos_samx = dev.samx.read()["samx"]["value"]
    current_pos_samy = dev.samy.read()["samy"]["value"]

    # make sure the new position is within 2x the tolerance (two movements)
    assert np.isclose(current_pos_samx, 10, atol=tolerance_samx * 2)
    assert np.isclose(current_pos_samy, 20, atol=tolerance_samy * 2)

    scans.umv(dev.samx, 20, dev.samy, -20)
    current_pos_samx = dev.samx.read()["samx"]["value"]
    current_pos_samy = dev.samy.read()["samy"]["value"]

    # make sure the umv movement is within the tolerance
    assert np.isclose(current_pos_samx, 20, atol=tolerance_samx)
    assert np.isclose(current_pos_samy, -20, atol=tolerance_samy)

    status = scans.grid_scan(
        dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.01, relative=False
    )

    # make sure the scan completed the expected number of points
    assert len(status.scan.data) == 100
    assert status.scan.num_points == 100

    # make sure the scan was absolute, not relative
    assert np.isclose(
        -5, status.scan.data[0].content["data"]["samx"]["samx"]["value"], atol=tolerance_samx
    )


@pytest.mark.timeout(200)
def test_scan_abort():
    def send_abort(bec):
        while True:
            if not bec.queue.current_scan:
                continue
            if len(bec.queue.current_scan.data) > 0:
                _thread.interrupt_main()
                break
        time.sleep(2)
        _thread.interrupt_main()

    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    aborted_scan = False
    try:
        threading.Thread(target=send_abort, args=(bec,), daemon=True).start()
        scans.line_scan(dev.samx, -5, 5, steps=200, exp_time=0.1)
    except ScanInterruption:
        bec.queue.request_scan_abortion()
        aborted_scan = True
    assert aborted_scan is True


@pytest.mark.timeout(200)
def test_limit_error():
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    aborted_scan = False
    dev.samx.limits = [-50, 50]
    try:
        scans.line_scan(dev.samx, -520, 5, steps=200, exp_time=0.1, relative=False)
    except AlarmBase as alarm:
        assert alarm.alarm_type == "LimitError"
        aborted_scan = True

    assert aborted_scan is True

    aborted_scan = False
    dev.samx.limits = [-50, 50]
    try:
        scans.umv(dev.samx, 500)
    except AlarmBase as alarm:
        assert alarm.alarm_type == "LimitError"
        aborted_scan = True

    assert aborted_scan is True


@pytest.mark.timeout(200)
def test_queued_scan():
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    s1 = scans.line_scan(dev.samx, -5, 5, steps=100, exp_time=0.1, hide_report=True)
    s2 = scans.line_scan(dev.samx, -5, 5, steps=50, exp_time=0.1, hide_report=True)

    while True:
        if not s1.scan or not s2.scan:
            continue
        if s1.scan.queue_info.status != "RUNNING":
            continue
        assert bec.queue.get_queue_position(s1.scan.queue_info.scanID) == 0
        assert bec.queue.get_queue_position(s2.scan.queue_info.scanID) == 1
        break
    while len(s2.scan.data) != 50:
        time.sleep(0.5)
