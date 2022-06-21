# import pytest
# from .devicemanager import DeviceManagerKOSS

# @pytest.fixture
# def device_manager():
#     return DeviceManagerKOSS()


# def dummy_devices():
#     devices = {"samx": {}}
#     devices["samx"]["status"] = {}
#     devices["samx"]["status"]["enabled"] = True
#     devices["samx"]["type"] = "SynAxis"
#     devices["samx"]["config"] = {}
#     devices["samx"]["config"]["name"] = "motor"
#     devices["samx"]["config"]["labels"] = "samx"
#     devices["samx"]["config"]["delay"] = 5
#     devices["samy"] = {}
#     devices["samy"]["status"] = {}
#     devices["samy"]["status"]["enabled"] = True
#     devices["samy"]["type"] = "SynAxis"
#     devices["samy"]["config"] = {}
#     devices["samy"]["config"]["name"] = "motor"
#     devices["samy"]["config"]["labels"] = "samy"
#     return devices


# def test__is_config_valid(device_manager):
#     assert device_manager._is_config_valid()

# @pytest.mark.parametrize('devs,device_manager', [(dummy_devices(), DeviceManagerKOSS())])
# def test__load_config(devs, device_manager):
#     device_manager._load_config(devs)
#     assert False
#
#
# def test_load_config_from_file():
#     assert False
#
#
# def test_post_config():
#     assert False
#
#
# def test_config_status_callback():
#     assert False
#
#
# def test_start_config_consumer():
#     assert False
#
#
# def test_stop_config_consumer():
#     assert False
