from bec_lib.core.devicemanager import Device
from bec_lib.scan_manager import ScanReport

# pylint:disable=undefined-variable
# pylint: disable=too-many-arguments


def dscan(
    motor1: Device, m1_from: float, m1_to: float, steps: int, exp_time: float, **kwargs
) -> ScanReport:
    """Relative line scan with one device.

    Args:
        motor1 (Device): Device that should be scanned.
        m1_from (float): Start position relative to the current position.
        m1_to (float): End position relative to the current position.
        steps (int): Number of steps.
        exp_time (float): Exposure time.

    Returns:
        ScanReport: Status object.

    Examples:
        >>> dscan(dev.motor1, -5, 5, 10, 0.1)
    """
    return scans.line_scan(
        motor1, m1_from, m1_to, steps=steps, exp_time=exp_time, relative=True, **kwargs
    )


def d2scan(
    motor1: Device,
    m1_from: float,
    m1_to: float,
    motor2: Device,
    m2_from: float,
    m2_to: float,
    steps: int,
    exp_time: float,
    **kwargs
) -> ScanReport:
    """Relative line scan with two devices.

    Args:
        motor1 (Device): First device that should be scanned.
        m1_from (float): Start position of the first device relative to its current position.
        m1_to (float): End position of the first device relative to its current position.
        motor2 (Device): Second device that should be scanned.
        m2_from (float): Start position of the second device relative to its current position.
        m2_to (float): End position of the second device relative to its current position.
        steps (int): Number of steps.
        exp_time (float): Exposure time

    Returns:
        ScanReport: Status object.

    Examples:
        >>> d2scan(dev.motor1, -5, 5, dev.motor2, -8, 8, 10, 0.1)
    """
    return scans.line_scan(
        motor1,
        m1_from,
        m1_to,
        motor2,
        m2_from,
        m2_to,
        steps=steps,
        exp_time=exp_time,
        relative=True,
        **kwargs
    )


def ascan(motor1, m1_from, m1_to, steps, exp_time, **kwargs):
    """Absolute line scan with one device.

    Args:
        motor1 (Device): Device that should be scanned.
        m1_from (float): Start position.
        m1_to (float): End position.
        steps (int): Number of steps.
        exp_time (float): Exposure time.

    Returns:
        ScanReport: Status object.

    Examples:
        >>> ascan(dev.motor1, -5, 5, 10, 0.1)
    """
    return scans.line_scan(
        motor1, m1_from, m1_to, steps=steps, exp_time=exp_time, relative=False, **kwargs
    )


def a2scan(motor1, m1_from, m1_to, motor2, m2_from, m2_to, steps, exp_time, **kwargs):
    """Absolute line scan with two devices.

    Args:
        motor1 (Device): First device that should be scanned.
        m1_from (float): Start position of the first device.
        m1_to (float): End position of the first device.
        motor2 (Device): Second device that should be scanned.
        m2_from (float): Start position of the second device.
        m2_to (float): End position of the second device.
        steps (int): Number of steps.
        exp_time (float): Exposure time

    Returns:
        ScanReport: Status object.

    Examples:
        >>> a2scan(dev.motor1, -5, 5, dev.motor2, -8, 8, 10, 0.1)
    """
    return scans.line_scan(
        motor1,
        m1_from,
        m1_to,
        motor2,
        m2_from,
        m2_to,
        steps=steps,
        exp_time=exp_time,
        relative=False,
        **kwargs
    )


def dmesh(motor1, m1_from, m1_to, m1_steps, motor2, m2_from, m2_to, m2_steps, exp_time, **kwargs):
    """Relative mesh scan (grid scan) with two devices.

    Args:
        motor1 (Device): First device that should be scanned.
        m1_from (float): Start position of the first device relative to its current position.
        m1_to (float): End position of the first device relative to its current position.
        m1_steps (int): Number of steps for motor1.
        motor2 (Device): Second device that should be scanned.
        m2_from (float): Start position of the second device relative to its current position.
        m2_to (float): End position of the second device relative to its current position.
        m2_steps (int): Number of steps for motor2.
        exp_time (float): Exposure time

    Returns:
        ScanReport: Status object.

    Examples:
        >>> dmesh(dev.motor1, -5, 5, 10, dev.motor2, -8, 8, 10, 0.1)
    """
    return scans.grid_scan(
        motor1,
        m1_from,
        m1_to,
        m1_steps,
        motor2,
        m2_from,
        m2_to,
        m2_steps,
        exp_time=exp_time,
        relative=True,
    )


def amesh(motor1, m1_from, m1_to, m1_steps, motor2, m2_from, m2_to, m2_steps, exp_time, **kwargs):
    """Absolute mesh scan (grid scan) with two devices.

    Args:
        motor1 (Device): First device that should be scanned.
        m1_from (float): Start position of the first device.
        m1_to (float): End position of the first device.
        m1_steps (int): Number of steps for motor1.
        motor2 (Device): Second device that should be scanned.
        m2_from (float): Start position of the second device.
        m2_to (float): End position of the second device.
        m2_steps (int): Number of steps for motor2.
        exp_time (float): Exposure time

    Returns:
        ScanReport: Status object.

    Examples:
        >>> amesh(dev.motor1, -5, 5, 10, dev.motor2, -8, 8, 10, 0.1)
    """
    return scans.grid_scan(
        motor1,
        m1_from,
        m1_to,
        m1_steps,
        motor2,
        m2_from,
        m2_to,
        m2_steps,
        exp_time=exp_time,
        relative=False,
    )


def umv(*args) -> ScanReport:
    """Updated absolute move (i.e. blocking) for one or more devices.

    Returns:
        ScanReport: Status object.

    Examples:
        >>> umv(dev.samx, 1)
        >>> umv(dev.samx, 1, dev.samy, 2)
    """
    return scans.umv(*args, relative=False)


def umvr(*args) -> ScanReport:
    """Updated relative move (i.e. blocking) for one or more devices.

    Returns:
        ScanReport: Status object.

    Examples:
        >>> umvr(dev.samx, 1)
        >>> umvr(dev.samx, 1, dev.samy, 2)
    """
    return scans.umv(*args, relative=True)


def mv(*args) -> ScanReport:
    """Absolute move for one or more devices.

    Returns:
        ScanReport: Status object.

    Examples:
        >>> mv(dev.samx, 1)
        >>> mv(dev.samx, 1, dev.samy, 2)
    """
    return scans.mv(*args, relative=False)


def mvr(*args) -> ScanReport:
    """Relative move for one or more devices.

    Returns:
        ScanReport: Status object.

    Examples:
        >>> mvr(dev.samx, 1)
        >>> mvr(dev.samx, 1, dev.samy, 2)
    """
    return scans.mv(*args, relative=True)
