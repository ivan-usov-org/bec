# pylint: disable=too-many-public-methods
from string import Template


class MessageEndpoints:
    # devices feedback
    _device_status = "internal/devices/status"
    _device_read = "internal/devices/read"
    _device_last_read = "internal/devices/last_read"
    _device_readback = "internal/devices/readback"
    _device_req_status = "internal/devices/req_status"

    # device config
    _device_config_request = "internal/devices/config_request"
    _device_config_request_response = "internal/devices/config_request_response"
    _device_config = "internal/devices/config"
    _device_info = "internal/devices/info"
    _device_staged = "internal/devices/staged"

    # scan queue
    _scan_queue_modification = "internal/queue/queue_modification"
    _scan_queue_modification_request = "internal/queue/queue_modification_request"
    _scan_queue_insert = "internal/queue/queue_insert"
    _scan_queue_request = "internal/queue/queue_request"
    _scan_queue_request_response = "internal/queue/queue_request_response"
    _scan_queue_status = "internal/queue/queue_status"
    _scan_queue_history = "internal/queue/queue_history"

    # scan info
    _scan_number = "scans/scan_number"
    _dataset_number = "scans/dataset_number"
    _scan_status = "scans/scan_status"
    _scan_status_list = "scans/scan_status_list"
    _available_scans = "scans/available_scans"
    _scan_segment = "scans/scan_segment"
    _bluesky_events = "scans/bluesky-events"
    _public_scan_info = Template("public/$scanID/scan_info")
    _public_scan_segment = Template("public/$scanID/scan_segment/$pointID")
    _public_scan_data = Template("public/$scanID/scan_data/$device/$pointID")
    _public_scan_baseline = Template("public/$scanID/scan_baseline")
    _public_file = Template("public/$scanID/file")

    # instructions
    _device_instructions = "internal/devices/instructions"
    _device_rpc = "internal/devices/rpc"
    _pre_scan_macros = "internal/pre_scan_macros"
    _post_scan_macros = "internal/post_scan_macros"

    # log
    _log = "internal/log"
    _alarms = "internal/alarms"

    # service
    _services_status = "internal/services/status"
    _metrics = "internal/services/metrics"

    # misc
    _public_global_vars = "public/vars"
    _observer = "internal/observer"

    ##########

    # devices feedback
    @classmethod
    def device_status(cls, device: str):
        return f"{cls._device_status}/{device}"

    @classmethod
    def device_read(cls, device: str):
        return f"{cls._device_read}/{device}"

    @classmethod
    def device_last_read(cls, device: str):
        return f"{cls._device_last_read}/{device}"

    @classmethod
    def device_readback(cls, device: str):
        return f"{cls._device_readback}/{device}"

    @classmethod
    def device_req_status(cls, device: str):
        return f"{cls._device_req_status}/{device}"

    # device config
    @classmethod
    def device_config_request(cls):
        return cls._device_config_request

    @classmethod
    def device_config_request_response(cls, RID: str):
        return f"{cls._device_config_request_response}/{RID}"

    @classmethod
    def device_config(cls):
        return cls._device_config

    @classmethod
    def device_info(cls, device: str):
        return f"{cls._device_info}/{device}"

    @classmethod
    def device_staged(cls, device: str):
        return f"{cls._device_staged}/{device}"

    # scan queue
    @classmethod
    def scan_queue_modification(cls):
        return cls._scan_queue_modification

    @classmethod
    def scan_queue_modification_request(cls):
        return cls._scan_queue_modification_request

    @classmethod
    def scan_queue_insert(cls):
        return cls._scan_queue_insert

    @classmethod
    def scan_queue_request(cls):
        return cls._scan_queue_request

    @classmethod
    def scan_queue_request_response(cls):
        return cls._scan_queue_request_response

    @classmethod
    def scan_queue_status(cls):
        return cls._scan_queue_status

    @classmethod
    def scan_queue_history(cls):
        return cls._scan_queue_history

    # scan info

    @classmethod
    def scan_number(cls):
        return cls._scan_number

    @classmethod
    def dataset_number(cls):
        return cls._dataset_number

    @classmethod
    def scan_status(cls):
        return cls._scan_status

    @classmethod
    def scan_status_list(cls):
        return cls._scan_status_list

    @classmethod
    def available_scans(cls):
        return cls._available_scans

    @classmethod
    def bluesky_events(cls):
        return cls._bluesky_events

    @classmethod
    def scan_segment(cls):
        return cls._scan_segment

    # instructions
    @classmethod
    def device_instructions(cls):
        return cls._device_instructions

    @classmethod
    def device_rpc(cls, rpc_id: str):
        return f"{cls._device_rpc}/{rpc_id}"

    @classmethod
    def pre_scan_macros(cls):
        return cls._pre_scan_macros

    @classmethod
    def post_scan_macros(cls):
        return cls._post_scan_macros

    @classmethod
    def public_scan_info(cls, scanID: str):
        return cls._public_scan_info.substitute(scanID=scanID)

    @classmethod
    def public_scan_segment(cls, scanID: str, pointID: int):
        return cls._public_scan_segment.substitute(scanID=scanID, pointID=pointID)

    @classmethod
    def public_scan_data(cls, scanID: str, device: str, pointID: str):
        return cls._public_scan_data.substitute(scanID=scanID, device=device, pointID=pointID)

    @classmethod
    def public_scan_baseline(cls, scanID: str):
        return cls._public_scan_baseline.substitute(scanID=scanID)

    @classmethod
    def public_file(cls, scanID: str):
        return cls._public_file.substitute(scanID=scanID)

    # log
    @classmethod
    def log(cls):
        return cls._log

    @classmethod
    def alarm(cls):
        return cls._alarms

    # service
    @classmethod
    def service_status(cls, service_id: str):
        return f"{cls._services_status}/{service_id}"

    @classmethod
    def metrics(cls, service_id: str):
        return f"{cls._metrics}/{service_id}"

    # misc
    @classmethod
    def global_vars(cls, var_name: str):
        return f"{cls._public_global_vars}/{var_name}"

    @classmethod
    def observer(cls):
        return cls._observer
