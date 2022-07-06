import _thread
import threading
import time

import pytest
from bec_client import BKClient
from bec_utils import RedisConnector, ServiceConfig
from bec_utils.bec_errors import ScanInterruption

CONFIG_PATH = "../test_config.yaml"


def start_client():
    config = ServiceConfig(CONFIG_PATH)
    bec = BKClient(
        [config.redis],
        RedisConnector,
        config.scibec,
    )
    bec.start()
    return bec


def test_grid_scan(capsys):
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    s = scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.01)
    assert len(s.scan.data) == 100
    assert s.scan.num_points == 100
    captured = capsys.readouterr()
    assert "finished. Scan ID" in captured.out


def test_fermat_scan(capsys):
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    s = scans.fermat_scan(dev.samx, -5, 5, dev.samy, -5, 5, step=0.5, exp_time=0.01)
    assert len(s.scan.data) == 199
    assert s.scan.num_points == 199
    captured = capsys.readouterr()
    assert "finished. Scan ID" in captured.out


def test_line_scan(capsys):
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    s = scans.line_scan(dev.samx, -5, 5, steps=10, exp_time=0.01)
    assert len(s.scan.data) == 10
    assert s.scan.num_points == 10
    captured = capsys.readouterr()
    assert "finished. Scan ID" in captured.out


def test_mv_scan(capsys):
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    scans.mv(dev.samx, 10, dev.samy, 20)
    current_pos_samx = dev.samx.read()
    current_pos_samy = dev.samy.read()
    assert current_pos_samx["samx"]["value"] == 10
    assert current_pos_samy["samy"]["value"] == 20
    scans.umv(dev.samx, 10, dev.samy, 20)
    captured = capsys.readouterr()
    ref_out_samx = "samx:     10.00 ━━━━━━━━━━━━━━━      10.00 /      10.00 / 100 % 0:00:00 0:00:00"
    ref_out_samy = "samy:     20.00 ━━━━━━━━━━━━━━━      20.00 /      20.00 / 100 % 0:00:00 0:00:00"
    assert ref_out_samx in captured.out
    assert ref_out_samy in captured.out


def test_mv_scan_mv():
    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    scans.mv(dev.samx, 10, dev.samy, 20)
    current_pos_samx = dev.samx.read()
    current_pos_samy = dev.samy.read()
    assert current_pos_samx["samx"]["value"] == 10
    assert current_pos_samy["samy"]["value"] == 20
    s = scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.01)
    assert len(s.scan.data) == 100
    assert s.scan.num_points == 100
    current_pos_samx = dev.samx.read()
    current_pos_samy = dev.samy.read()
    assert current_pos_samx["samx"]["value"] == 10
    assert current_pos_samy["samy"]["value"] == 20
    scans.umv(dev.samx, 20, dev.samy, -20)
    s = scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.01)
    assert len(s.scan.data) == 100
    assert s.scan.num_points == 100
    current_pos_samx = dev.samx.read()
    current_pos_samy = dev.samy.read()
    assert current_pos_samx["samx"]["value"] == 20
    assert current_pos_samy["samy"]["value"] == -20


def test_scan_abort():
    def send_abort():
        time.sleep(2)
        _thread.interrupt_main()
        time.sleep(2)
        _thread.interrupt_main()

    bec = start_client()
    scans = bec.scans
    dev = bec.devicemanager.devices
    try:
        threading.Thread(target=send_abort, daemon=True).start()
        s = scans.line_scan(dev.samx, -5, 5, steps=100, exp_time=0.01)
    except ScanInterruption as scan_int:
        bec.queue.request_scan_abortion()
