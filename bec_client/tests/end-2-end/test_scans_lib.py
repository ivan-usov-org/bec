import time

import numpy as np
import pytest
from bec_lib import BECClient, RedisConnector, ServiceConfig, bec_logger
from bec_lib.alarm_handler import AlarmBase
from bec_lib.tests.utils import wait_for_empty_queue

logger = bec_logger.logger

CONFIG_PATH = "../ci/test_config.yaml"
# CONFIG_PATH = "../bec_config_dev.yaml"
# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
# pylint: disable=undefined-variable


@pytest.fixture(scope="function")
def lib_client():
    config = ServiceConfig(CONFIG_PATH)
    bec = BECClient(forced=True)
    bec.initialize(config, RedisConnector)
    bec.start()
    bec.queue.request_queue_reset()
    bec.queue.request_scan_continuation()
    time.sleep(5)
    yield bec
    bec.shutdown()


@pytest.mark.timeout(100)
def test_grid_scan_lib_client(lib_client):
    bec = lib_client
    scans = bec.scans
    wait_for_empty_queue(bec)
    bec.metadata.update({"unit_test": "test_grid_scan_lib_client"})
    dev = bec.device_manager.devices
    scans.umv(dev.samx, 0, dev.samy, 0, relative=False)
    status = scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.01, relative=True)
    status.wait()
    assert len(status.scan.data) == 100
    assert status.scan.num_points == 100


@pytest.mark.timeout(100)
def test_mv_scan_lib_client(lib_client):
    bec = lib_client
    scans = bec.scans
    wait_for_empty_queue(bec)
    bec.metadata.update({"unit_test": "test_mv_scan_lib_client"})
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


@pytest.mark.timeout(100)
def test_mv_raises_limit_error(lib_client):
    bec = lib_client
    scans = bec.scans
    wait_for_empty_queue(bec)
    bec.metadata.update({"unit_test": "test_mv_raises_limit_error"})
    dev = bec.device_manager.devices
    dev.samx.limits = [-50, 50]
    with pytest.raises(AlarmBase) as exc:
        scans.mv(dev.samx, 1000, relative=False).wait()


@pytest.mark.timeout(100)
def test_async_callback_data_matches_scan_data_lib_client(lib_client):
    bec = lib_client
    wait_for_empty_queue(bec)
    bec.metadata.update({"unit_test": "test_async_callback_data_matches_scan_data"})
    dev = bec.device_manager.devices
    reference_container = {"data": [], "metadata": {}}

    def dummy_callback(data, metadata):
        logger.info(f"callback metadata: {metadata}")
        reference_container["metadata"] = metadata
        reference_container["data"].append(data)

    s = scans.line_scan(dev.samx, 0, 1, steps=10, relative=False, async_callback=dummy_callback)
    s.wait()
    while len(reference_container["data"]) < 10:
        time.sleep(0.1)
    assert len(s.scan.data) == 10
    assert len(reference_container["data"]) == 10

    for ii, msg in enumerate(s.scan.data.messages.values()):
        assert msg.content == reference_container["data"][ii]


@pytest.mark.timeout(100)
def test_config_updates(lib_client):
    bec = lib_client
    wait_for_empty_queue(bec)
    bec.metadata.update({"unit_test": "test_config_updates"})
    dev = bec.device_manager.devices
    dev.samx.limits = [-80, 80]
    assert dev.samx.limits == [-80, 80]
    dev.samx.limits = [-50, 50]
    assert dev.samx.limits == [-50, 50]

    dev.samx.velocity.set(10)
    assert dev.samx.velocity.read()["samx_velocity"]["value"] == 10
    assert dev.samx.velocity.read(cached=False)["samx_velocity"]["value"] == 10
    assert dev.samx.read_configuration()["samx_velocity"]["value"] == 10
    assert dev.samx.read_configuration(cached=False)["samx_velocity"]["value"] == 10

    assert dev.samx.dummy_controller.some_var == 10
    dev.samx.dummy_controller.some_var = 20
    assert dev.samx.dummy_controller.some_var == 20
