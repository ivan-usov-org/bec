import os
import threading
import time

import numpy as np
import pytest
import yaml

import bec_lib
from bec_lib import BECClient, DeviceConfigError, RedisConnector, ServiceConfig, bec_logger
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


@pytest.fixture()
def threads_check():
    current_threads = set(th for th in threading.enumerate() if th is not threading.main_thread())
    yield
    threads_after = set(th for th in threading.enumerate() if th is not threading.main_thread())
    additional_threads = threads_after - current_threads
    assert (
        len(additional_threads) == 0
    ), f"Test creates {len(additional_threads)} threads that are not cleaned: {additional_threads}"


@pytest.fixture(scope="function")
def lib_client(threads_check):
    config = ServiceConfig(CONFIG_PATH)
    bec = BECClient(config, RedisConnector, forced=True)
    bec.start()
    bec.queue.request_queue_reset()
    bec.queue.request_scan_continuation()
    time.sleep(5)
    yield bec
    bec.shutdown()
    bec._client._reset_singleton()


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

    dev.samx.velocity.set(10).wait()
    assert dev.samx.velocity.read()["samx_velocity"]["value"] == 10
    assert dev.samx.velocity.read(cached=False)["samx_velocity"]["value"] == 10
    assert dev.samx.read_configuration()["samx_velocity"]["value"] == 10
    assert dev.samx.read_configuration(cached=False)["samx_velocity"]["value"] == 10

    dev.samx.velocity.put(5)
    assert dev.samx.velocity.get() == 5

    dev.samx.velocity.set(10).wait()
    assert dev.samx.velocity.get() == 10

    dev.samx.setpoint.put(5)
    assert dev.samx.setpoint.get() == 5

    dev.samx.setpoint.set(10).wait()
    assert dev.samx.setpoint.get() == 10
    assert dev.samx.dummy_controller.some_var == 10
    dev.samx.dummy_controller.some_var = 20
    assert dev.samx.dummy_controller.some_var == 20
    dev.samx.dummy_controller.some_var = 10
    val = dev.samx.readback.get()
    assert np.isclose(val, dev.samx.position, atol=0.05)


@pytest.mark.timeout(100)
def test_dap_fit(lib_client):
    bec = lib_client
    wait_for_empty_queue(bec)
    bec.metadata.update({"unit_test": "test_dap_fit"})
    dev = bec.device_manager.devices
    scans = bec.scans

    dev.bpm4i.sim.sim_select_model("GaussianModel")
    params = dev.bpm4i.sim.sim_params
    params.update(
        {"noise": "uniform", "noise_multiplier": 10, "center": 5, "sigma": 1, "amplitude": 200}
    )
    dev.bpm4i.sim.sim_params = params
    time.sleep(1)

    res = scans.line_scan(dev.samx, 0, 8, steps=50, relative=False)
    res.wait()

    fit = bec.dap.GaussianModel.fit(res.scan, "samx", "samx", "bpm4i", "bpm4i")

    assert np.isclose(fit.center, 5, atol=0.5)


@pytest.mark.timeout(100)
@pytest.mark.parametrize(
    "config, raises_error, deletes_config, disabled_device",
    [
        (
            {
                "hexapod": {
                    "deviceClass": "SynDeviceOPAAS",
                    "deviceConfig": {},
                    "deviceTags": ["user motors"],
                    "readoutPriority": "baseline",
                    "enabled": True,
                    "readOnly": False,
                },
                "eyefoc": {
                    "deviceClass": "SimPositioner",
                    "deviceConfig": {
                        "delay": 1,
                        "limits": [-50, 50],
                        "speed": 100,
                        "tolerance": 0.01,
                        "update_frequency": 400,
                    },
                    "deviceTags": ["user motors"],
                    "enabled": True,
                    "readOnly": False,
                },
            },
            True,
            False,
            [],
        ),
        (
            {
                "hexapod": {
                    "deviceClass": "SynDeviceOPAAS",
                    "deviceConfig": {},
                    "deviceTags": ["user motors"],
                    "readoutPriority": "baseline",
                    "enabled": True,
                    "readOnly": False,
                },
                "eyefoc": {
                    "deviceClass": "SimPositioner",
                    "deviceConfig": {
                        "delay": 1,
                        "limits": [-50, 50],
                        "speed": 100,
                        "tolerance": 0.01,
                        "update_frequency": 400,
                    },
                    "readoutPriority": "baseline",
                    "deviceTags": ["user motors"],
                    "enabled": True,
                    "readOnly": False,
                },
            },
            False,
            False,
            [],
        ),
        (
            {
                "hexapod": {
                    "deviceClass": "SynDeviceOPAAS",
                    "deviceConfig": {},
                    "deviceTags": ["user motors"],
                    "readoutPriority": "baseline",
                    "enabled": True,
                    "readOnly": False,
                },
                "eyefoc": {
                    "deviceClass": "utils:bec_utils:DeviceClassConnectionError",
                    "deviceConfig": {},
                    "readoutPriority": "baseline",
                    "deviceTags": ["user motors"],
                    "enabled": True,
                    "readOnly": False,
                },
            },
            True,
            False,
            ["eyefoc"],
        ),
        (
            {
                "hexapod": {
                    "deviceClass": "SynDeviceOPAAS",
                    "deviceConfig": {},
                    "deviceTags": ["user motors"],
                    "readoutPriority": "baseline",
                    "enabled": True,
                    "readOnly": False,
                },
                "eyefoc": {
                    "deviceClass": "utils:bec_utils:DeviceClassInitError",
                    "deviceConfig": {},
                    "readoutPriority": "baseline",
                    "deviceTags": ["user motors"],
                    "enabled": True,
                    "readOnly": False,
                },
            },
            True,
            True,
            [],
        ),
        (
            {
                "hexapod": {
                    "deviceClass": "SynDeviceOPAAS",
                    "deviceConfig": {},
                    "deviceTags": ["user motors"],
                    "readoutPriority": "baseline",
                    "enabled": True,
                    "readOnly": False,
                },
                "eyefoc": {
                    "deviceClass": "WrongDeviceClass",
                    "deviceConfig": {},
                    "readoutPriority": "baseline",
                    "deviceTags": ["user motors"],
                    "enabled": True,
                    "readOnly": False,
                },
            },
            True,
            True,
            [],
        ),
    ],
    ids=[
        "invalid_config_missing_readoutPriority",
        "valid_config_no_error",
        "invalid_device_class_connection_error",
        "invalid_device_class_init",
        "invalid_device_class",
    ],
)
def test_config_reload(lib_client, config, raises_error, deletes_config, disabled_device):
    bec = lib_client
    wait_for_empty_queue(bec)
    bec.metadata.update({"unit_test": "test_config_reload"})
    try:
        # write new config to disk
        with open("./e2e_runtime_config_test.yaml", "w") as f:
            f.write(yaml.dump(config))
        num_devices = len(bec.device_manager.devices)
        if raises_error:
            with pytest.raises(DeviceConfigError):
                bec.config.update_session_with_file("./e2e_runtime_config_test.yaml")
            if deletes_config:
                assert len(bec.device_manager.devices) == 0
            elif disabled_device:
                assert len(bec.device_manager.devices) == 2
            else:
                assert len(bec.device_manager.devices) == num_devices
        else:
            bec.config.update_session_with_file("./e2e_runtime_config_test.yaml")
            assert len(bec.device_manager.devices) == 2
        for dev in disabled_device:
            assert bec.device_manager.devices[dev].enabled is False
    finally:
        test_device_config = os.path.join(
            os.path.dirname(os.path.abspath(bec_lib.tests.__file__)), "test_config.yaml"
        )
        bec.config.update_session_with_file(test_device_config)
    # bec.config.load_demo_config()


def test_computed_signal(lib_client):
    bec = lib_client
    wait_for_empty_queue(bec)
    bec.metadata.update({"unit_test": "test_computed_signal"})
    dev = bec.device_manager.devices
    scans = bec.scans

    res = scans.line_scan(dev.samx, -0.1, 0.1, steps=10, relative=False, exp_time=0)
    res.wait()
    assert "pseudo_signal1" in res.scan.baseline

    def compute_signal1(*args, **kwargs):
        return 5

    dev.pseudo_signal1.set_compute_method(compute_signal1)
    dev.pseudo_signal1.set_input_signals()

    assert dev.pseudo_signal1.read(cached=False)["pseudo_signal1"]["value"] == 5
