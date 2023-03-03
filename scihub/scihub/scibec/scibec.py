import functools
import json

import requests
import yaml
from bec_utils.logger import bec_logger

logger = bec_logger.logger


class SciBecError(Exception):
    pass


class SciBec:
    url = "http://[::1]:3030"

    def __init__(self):
        self.client = HttpClient()

    def patch_device_config(self, id, config) -> bool:
        headers = {"Content-type": "application/json"}
        return self.client.patch_request(
            f"{self.url}/devices/{id}", headers=headers, payload=config
        )

    def get_beamlines(self, params=None) -> list:
        headers = {"Content-type": "application/json"}
        return self.client.get_request(f"{self.url}/beamlines", headers=headers, params=params)

    def get_beamline(self, beamline: str, raise_none=False) -> dict:
        params = self.client.make_filter(
            where={"name": beamline}, include=[{"relation": "sessions"}]
        )
        beamline = self.get_beamlines(params=params)

        if not beamline:
            if raise_none:
                raise SciBecError("Failed to retrieve beamline info.")
            return None
        if len(beamline) > 1:
            logger.warning(
                f"Found more than one entry for beamline {beamline}. Only the first entry will be considered."
            )
        return beamline[0]

    def add_beamline(self, name: str) -> bool:
        available_beamlines = self.get_beamlines()
        for beamline in available_beamlines:
            if beamline.get("name") == name:
                raise SciBecError("A beamline with the same name already exists.")
        headers = {"Content-type": "application/json"}
        return self.client.post_request(
            f"{self.url}/beamlines", headers=headers, payload={"name": name}
        )

    def _delete_beamline(self, beamline_id: str):
        return self.client.delete_request(f"{self.url}/beamlines/{beamline_id}")

    def get_available_sessions(self, beamline: str) -> list:
        headers = {"Content-type": "application/json"}
        params = self.client.make_filter(
            include=[{"relation": "sessions"}], where={"name": beamline}
        )
        return self.client.get_request(f"{self.url}/beamlines", params=params, headers=headers)

    def add_session(self, beamline: str, session: str):
        beamline = self.get_beamline(beamline, raise_none=True)

        headers = {"Content-type": "application/json"}
        obj = {
            "ownerGroup": "test",
            "accessGroups": ["customer"],
            "name": session,
            "beamlineId": beamline["id"],
        }
        return self.client.post_request(f"{self.url}/sessions", payload=obj, headers=headers)

    def get_session_by_id(self, session_id: str, include_devices=False):
        headers = {"Content-type": "application/json"}
        include = [{"relation": "devices"}] if include_devices else None
        params = self.client.make_filter(where={"id": session_id}, include=include)
        return self.client.get_request(f"{self.url}/sessions", params=params, headers=headers)

    def get_session_by_name(self, beamline: str, session: str, include_devices=False):
        beamline = self.get_beamline(beamline, raise_none=True)
        headers = {"Content-type": "application/json"}
        include = [{"relation": "devices"}] if include_devices else None
        params = self.client.make_filter(
            where={"name": session, "beamlineId": beamline["id"]}, include=include
        )
        return self.client.get_request(f"{self.url}/sessions", params=params, headers=headers)

    def get_current_session(self, beamline: str, include_devices=False):
        beamline_info = self.get_beamline(beamline, raise_none=True)
        if not beamline_info.get("activeSession"):
            return
        session = self.get_session_by_id(
            beamline_info["activeSession"], include_devices=include_devices
        )
        if session:
            return session[0]
        return

    def set_current_session(self, beamline: str, session: str):
        headers = {"Content-type": "application/json"}
        beamline = self.get_beamline(beamline, raise_none=True)
        if not "sessions" in beamline:
            raise SciBecError(f"Beamline {beamline} has no sessions.")
        target_session = None
        for avail_session in beamline["sessions"]:
            if avail_session["name"] == session:
                target_session = avail_session
        if not target_session:
            raise SciBecError(f"Beamline {beamline} has no session {session}.")
        update_obj = {"activeSession": target_session["id"]}
        self.client.patch_request(
            f"{self.url}/beamlines/{beamline['id']}", headers=headers, payload=update_obj
        )

    def _delete_session(self, session_id: str):
        return self.client.delete_request(f"{self.url}/sessions/{session_id}")

    def add_device(self, device_info: dict):
        headers = {"Content-type": "application/json"}
        try:
            res = self.client.post_request(
                f"{self.url}/devices", payload=device_info, headers=headers
            )
        except Exception as exc:
            print(f"Failed to add device with device_info: {device_info}.")
            raise exc
        return res

    def _delete_device(self, device_id: str):
        return self.client.delete_request(f"{self.url}/devices/{device_id}")

    def load_config_from_file(self, file_path: str) -> dict:
        data = {}
        if file_path.endswith(".yaml"):
            with open(file_path, "r") as stream:
                try:
                    data = yaml.safe_load(stream)
                    logger.trace(
                        f"Loaded new config from disk: {json.dumps(data, sort_keys=True, indent=4)}"
                    )
                except yaml.YAMLError as er:
                    logger.error(f"Error while loading config from disk: {repr(er)}")
        # elif file_path.endswith(".json"):
        #     with open(file_path) as stream:
        #         try:
        #             data = json.load(stream)
        #             logger.trace(
        #                 f"Loaded new config from disk: {json.dumps(data, sort_keys=True, indent=4)}"
        #             )
        #         except json.JSONDecodeError as er:
        #             logger.error(f"Error while loading config from disk: {repr(er)}")
        else:
            raise NotImplementedError

        return data

    def update_session_with_file(self, file_path: str):
        data = self.load_config_from_file(file_path)
        beamlines = self.get_beamlines()
        if not beamlines:
            logger.warning("No config available.")
            return
        if len(beamlines) > 1:
            logger.warning("More than one beamline available.")
        beamline = beamlines[0]
        self.set_session_data(beamline, data)

    def set_session_data(self, beamline: dict, data: dict):
        session_name = "demo"
        if beamline.get("activeSession"):
            session = self.get_session_by_id(beamline["activeSession"])
            if session:
                session_name = session[0]["name"]
                self._delete_session(session[0]["id"])
        session = self.add_session(beamline["name"], session_name)
        self.set_current_session(beamline["name"], session_name)
        for name, device in data.items():
            device["enabled"] = device["status"]["enabled"]
            if device["status"].get("enabled_set"):
                device["enabled_set"] = device["status"].get("enabled_set")
            device.pop("status")
            device["name"] = name
            device["sessionId"] = session["id"]
            self.add_device(device)


def authenticated(func):
    @functools.wraps(func)
    def authenticated_call(client, *args, **kwargs):
        # if not isinstance(client, HttpClient):
        #     raise AttributeError("First argument must be an instance of HttpClient")
        # if "headers" in kwargs:
        #     kwargs["headers"] = kwargs["headers"].copy()
        # else:
        #     kwargs["headers"] = {}
        # kwargs["headers"]["Authorization"] = client.token
        return func(client, *args, **kwargs)

    return authenticated_call


def formatted_http_error(func):
    @functools.wraps(func)
    def formatted_call(*args, **kwargs):
        try:
            out = func(*args, **kwargs)
        except requests.HTTPError as exc:
            raise SciBecError(f"{exc.response.reason} Error Message: {exc.response.text}") from exc
        return out

    return formatted_call


class HttpClient:
    def __init__(self, *args, **kwargs):
        self._verify_certificate = False
        super().__init__(*args, **kwargs)

    def authenticate(self, username, password):
        raise NotImplementedError

    @authenticated
    @formatted_http_error
    def get_request(self, url, params=None, headers=None, timeout=10):
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
            verify=self._verify_certificate,
        )
        response.raise_for_status()
        return response.json()

    @authenticated
    @formatted_http_error
    def post_request(self, url, payload=None, files=None, headers=None, timeout=10):
        req = requests.post(
            url,
            json=payload,
            files=files,
            headers=headers,
            timeout=timeout,
            verify=self._verify_certificate,
        )
        req.raise_for_status()
        return req.json()

    @authenticated
    @formatted_http_error
    def patch_request(self, url, payload=None, files=None, headers=None, timeout=10):
        req = requests.patch(
            url,
            json=payload,
            files=files,
            headers=headers,
            timeout=timeout,
            verify=self._verify_certificate,
        )
        req.raise_for_status()
        return req.ok

    @authenticated
    @formatted_http_error
    def delete_request(self, url, headers=None, timeout=10):
        req = requests.delete(
            url,
            headers=headers,
            timeout=timeout,
            verify=self._verify_certificate,
        )
        req.raise_for_status()
        return req.ok

    @staticmethod
    def make_filter(
        where: dict = None,
        limit: int = 0,
        skip: int = 0,
        fields: dict = None,
        include: list = None,
        order: list = None,
    ) -> dict:
        """_summary_

        Args:
            where (dict, optional): Where filter. Defaults to None.
            limit (int, optional): Limit filter. Defaults to 0.
            skip (int, optional): skip entries. Defaults to 0.
            fields (dict, optional): Include only certain fields. Defaults to None.
            include (list, optional): Include embedded documents. Defaults to None.
            order (list, optional): Order of documents. Defaults to None.

        Returns:
            dict: Filter dictionary
        """
        filt = {}
        if where is not None:
            items = [where.copy()]
            filt["where"] = {"and": items}
        if limit > 0:
            filt["limit"] = limit
        if skip > 0:
            filt["skip"] = skip
        if fields is not None:
            filt["fields"] = fields
        if order is not None:
            filt["order"] = order
        if include is not None:
            filt["include"] = include
        filt = json.dumps(filt)
        return {"filter": filt}
