from unittest import mock

from bec_client.plugins.LamNI import LamNI, XrayEyeAlign
from bec_lib.device import Device

# pylint: disable=unused-import
from bec_lib.tests.utils import bec_client

# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access


class RTControllerMock:
    def feedback_disable(self):
        pass

    def feedback_enable_with_reset(self):
        pass


class RTMock(Device):
    controller = RTControllerMock()
    enabled = True


def test_save_frame(bec_client):
    client = bec_client
    client.device_manager.devices.xeye = Device("xeye", {})
    lamni = LamNI(client)
    align = XrayEyeAlign(client, lamni)
    with mock.patch("bec_client.plugins.LamNI.x_ray_eye_align.epics_put") as epics_put_mock:
        align.save_frame()
        epics_put_mock.assert_called_once_with("XOMNYI-XEYE-SAVFRAME:0", 1)


def test_update_frame(bec_client):
    epics_put = "bec_client.plugins.LamNI.x_ray_eye_align.epics_put"
    epics_get = "bec_client.plugins.LamNI.x_ray_eye_align.epics_get"
    fshopen = "bec_client.plugins.LamNI.x_ray_eye_align.fshopen"
    client = bec_client
    client.device_manager.devices.xeye = Device("xeye", {})
    lamni = LamNI(client)
    align = XrayEyeAlign(client, lamni)
    with mock.patch(epics_put) as epics_put_mock:
        with mock.patch(epics_get) as epics_get_mock:
            with mock.patch(fshopen) as fshopen_mock:
                align.update_frame()
                epics_put_mock.assert_has_calls(
                    [
                        mock.call("XOMNYI-XEYE-ACQDONE:0", 0),
                        mock.call("XOMNYI-XEYE-ACQ:0", 1),
                        mock.call("XOMNYI-XEYE-ACQDONE:0", 0),
                        mock.call("XOMNYI-XEYE-ACQ:0", 0),
                    ]
                )
                fshopen_mock.assert_called_once()
                epics_get_mock.assert_called_with("XOMNYI-XEYE-ACQDONE:0")


def test_disable_rt_feedback(bec_client):
    client = bec_client
    client.device_manager.devices.xeye = Device("xeye", {})
    lamni = LamNI(client)
    align = XrayEyeAlign(client, lamni)
    client.device_manager.devices.rtx = RTMock("rtx", {})
    with mock.patch.object(
        align.device_manager.devices.rtx.controller, "feedback_disable"
    ) as fdb_disable:
        align._disable_rt_feedback()
        fdb_disable.assert_called_once()


def test_enable_rt_feedback(bec_client):
    client = bec_client
    client.device_manager.devices.xeye = Device("xeye", {})
    lamni = LamNI(client)
    align = XrayEyeAlign(client, lamni)
    client.device_manager.devices.rtx = RTMock("rtx", {})
    with mock.patch.object(
        align.device_manager.devices.rtx.controller, "feedback_enable_with_reset"
    ) as fdb_enable:
        align._enable_rt_feedback()
        fdb_enable.assert_called_once()


def test_tomo_rotate(bec_client):
    import builtins

    client = bec_client
    client.load_high_level_interface("spec_hli")
    client.device_manager.devices.xeye = Device("xeye", {})
    lamni = LamNI(client)
    align = XrayEyeAlign(client, lamni)
    client.device_manager.devices.lsamrot = RTMock("lsamrot", {})
    with mock.patch.object(builtins, "umv") as umv:
        align.tomo_rotate(5)
        umv.assert_called_once_with(client.device_manager.devices.lsamrot, 5)
