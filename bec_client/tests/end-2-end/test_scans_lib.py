import _thread
import threading
import time

import numpy as np
import pytest
from bec_client_lib import BECClient
from bec_client_lib.alarm_handler import AlarmBase
from bec_utils import (
    BECMessage,
    MessageEndpoints,
    RedisConnector,
    ServiceConfig,
    bec_logger,
)
from bec_utils.bec_errors import ScanAbortion, ScanInterruption

from .test_scans import get_queue, queue_is_empty, wait_for_empty_queue

logger = bec_logger.logger

CONFIG_PATH = "../ci/test_config.yaml"
# CONFIG_PATH = "../bec_config_dev.yaml"
# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
# pylint: disable=undefined-variable


@pytest.fixture(scope="module", autouse=True)
def client():
    config = ServiceConfig(CONFIG_PATH)
    bec = BECClient(forced=True)
    bec.initialize(
        config,
        RedisConnector,
    )
    bec.start()
    bec.queue.request_queue_reset()
    bec.queue.request_scan_continuation()
    time.sleep(5)
    yield bec
    bec.shutdown()


@pytest.mark.timeout(100)
def test_grid_scan(client):
    bec = client
    scans = bec.scans
    wait_for_empty_queue(bec)
    bec.metadata.update({"unit_test": "test_grid_scan"})
    dev = bec.device_manager.devices
    scans.umv(dev.samx, 0, dev.samy, 0, relative=False)
    status = scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.01, relative=True)
    status.wait()
    assert len(status.scan.data) == 100
    assert status.scan.num_points == 100


@pytest.mark.timeout(100)
def test_mv_scan(client):
    bec = client
    scans = bec.scans
    wait_for_empty_queue(bec)
    bec.metadata.update({"unit_test": "test_mv_scan"})
    dev = bec.device_manager.devices
    scans.mv(dev.samx, 10, dev.samy, 20, relative=False).wait()
    current_pos_samx = dev.samx.read()["samx"]["value"]
    current_pos_samy = dev.samy.read()["samy"]["value"]
    assert np.isclose(
        current_pos_samx, 10, atol=dev.samx._config["deviceConfig"].get("tolerance", 0.05)
    )
    assert np.isclose(
        current_pos_samy, 20, atol=dev.samy._config["deviceConfig"].get("tolerance", 0.05)
    )
