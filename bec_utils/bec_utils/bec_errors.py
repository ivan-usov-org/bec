class ScanAbortion(Exception):
    pass


class ScanInterruption(Exception):
    pass


class ServiceConfigError(Exception):
    pass


class DeviceConfigError(Exception):
    pass


class ScanRequestError(Exception):
    pass


class RPCError(Exception):
    pass
