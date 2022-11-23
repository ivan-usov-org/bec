import os
from unittest import mock

import pytest

import bec_utils
from bec_utils.scibec import HttpClient, SciBec, SciBecError

dir_path = os.path.dirname(bec_utils.__file__)


def test_make_filter():
    httpclient = HttpClient()
    filter = httpclient.make_filter(where={"ownerGroup": "p12345"})
    assert filter == {"filter": '{"where": {"and": [{"ownerGroup": "p12345"}]}}'}


def test_load_from_file():
    file_path = f"{dir_path}/tests/test_config.yaml"
    scibec = SciBec()
    config = scibec.load_config_from_file(file_path)
    assert {"acquisitionConfig", "deviceClass", "deviceTags", "deviceConfig", "status"} == set(
        config["samx"].keys()
    )


def test_get_beamlines():
    scibec = SciBec()
    with mock.patch.object(scibec.client, "get_request") as get_request:
        scibec.get_beamlines()
        get_request.assert_called_once()


def test_get_beamlines_filter():
    scibec = SciBec()
    with mock.patch.object(scibec.client, "get_request") as get_request:
        params = {"where": {"ownerGroup": "p12345"}}
        scibec.get_beamlines(params=params)
        get_request.assert_called_once_with(
            f"{scibec.url}/beamlines", headers={"Content-type": "application/json"}, params=params
        )


def test_get_beamline():
    scibec = SciBec()
    with mock.patch.object(scibec.client, "get_request", return_value=[]) as get_request:
        scibec.get_beamline("test_beamline")
        get_request.assert_called_once()

    with mock.patch.object(scibec.client, "get_request", return_value=[]) as get_request:
        with pytest.raises(SciBecError):
            scibec.get_beamline("test_beamline", raise_none=True)
            get_request.assert_called_once()

    with mock.patch.object(
        scibec.client, "get_request", return_value=["test_beamline"]
    ) as get_request:
        val = scibec.get_beamline("test_beamline", raise_none=True)
        assert val == "test_beamline"


def test_add_beamline():
    scibec = SciBec()
    with mock.patch.object(
        scibec.client, "get_request", return_value=[{"name": "test_beamline"}]
    ) as get_request:
        with pytest.raises(SciBecError):
            scibec.add_beamline("test_beamline")

        with mock.patch.object(scibec.client, "post_request") as post_request:
            scibec.add_beamline("test_beamline2")
            post_request.assert_called_once()


def test_delete_beamline():
    scibec = SciBec()
    with mock.patch.object(scibec.client, "delete_request") as delete_request:
        scibec._delete_beamline("beamlineID")
        delete_request.assert_called_once_with(f"{scibec.url}/beamlines/beamlineID")


def test_update_session_with_file():
    scibec = SciBec()
    file_path = f"{dir_path}/tests/test_config.yaml"
    with mock.patch.object(scibec, "get_beamlines", return_value=[]):
        scibec.update_session_with_file(file_path)
    with mock.patch.object(scibec, "get_beamlines", return_value=[{"name": "test_beamline"}]):
        with mock.patch.object(scibec, "add_session", return_value={"id": "sessionID"}):
            with mock.patch.object(scibec, "set_current_session") as set_session:
                with mock.patch.object(scibec, "add_device"):
                    scibec.update_session_with_file(file_path)


def test_set_current_session():
    scibec = SciBec()
    with mock.patch.object(scibec, "get_beamline", return_value=[]):
        with pytest.raises(SciBecError):
            scibec.set_current_session("test_beamline", "demo")
    with mock.patch.object(
        scibec,
        "get_beamline",
        return_value=[{"name": "test_beamline", "sessions": []}],
    ):
        with pytest.raises(SciBecError):
            scibec.set_current_session("test_beamline", "demo")

    with mock.patch.object(
        scibec,
        "get_beamlines",
        return_value=[
            {
                "name": "test_beamline",
                "id": "beamlineID",
                "sessions": [{"id": "sessionID", "name": "demo"}],
            }
        ],
    ):
        with mock.patch.object(scibec.client, "patch_request") as patch_request:
            scibec.set_current_session("test_beamline", "demo")
            patch_request.assert_called_once()
