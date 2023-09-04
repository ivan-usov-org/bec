import builtins
import datetime
import threading
import time
from abc import ABC, abstractmethod

from typeguard import typechecked

from bec_lib.core import bec_logger
from bec_lib.core.devicemanager import Device

logger = bec_logger.logger


class BeamlineCondition(ABC):
    """Abstract base class for beamline checks."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enabled = True

    @property
    @abstractmethod
    def name(self) -> str:
        """Return a name for the beamline check."""

    @abstractmethod
    def run(self) -> bool:
        """Run the beamline check and return True if the beam is okay, False otherwise."""

    @abstractmethod
    def on_failure_msg(self) -> str:
        """Return a message that will be displayed if the beamline check fails."""


class ShutterCondition(BeamlineCondition):
    """Check if the shutter is open."""

    def __init__(self, shutter: Device):
        super().__init__()
        self.shutter = shutter

    @property
    def name(self):
        return "shutter"

    def run(self):
        shutter_val = self.shutter.read(cached=True)
        return shutter_val["value"].lower() == "open"

    def on_failure_msg(self):
        return "Check beam failed: Shutter is closed."


class LightAvailableCondition(BeamlineCondition):
    """Check if the light is available."""

    def __init__(self, machine_status: Device):
        super().__init__()
        self.machine_status = machine_status

    @property
    def name(self):
        return "light_available"

    def run(self):
        machine_status = self.machine_status.read(cached=True)
        return machine_status["value"] in ["Light Available", "Light-Available"]

    def on_failure_msg(self):
        return "Check beam failed: Light not available."


class FastOrbitFeedbackCondition(BeamlineCondition):
    """Check if the fast orbit feedback is running."""

    def __init__(self, sls_fast_orbit_feedback: Device):
        super().__init__()
        self.sls_fast_orbit_feedback = sls_fast_orbit_feedback

    @property
    def name(self):
        return "fast_orbit_feedback"

    def run(self):
        fast_orbit_feedback = self.sls_fast_orbit_feedback.read(cached=True)
        return fast_orbit_feedback["value"] == "running"

    def on_failure_msg(self):
        return "Check beam failed: Fast orbit feedback is not running."


class BeamlineChecks:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = builtins.__dict__.get("bec")
        self.send_to_scilog = True
        self._beam_is_okay = True
        self._beamline_checks = {}
        self._stop_beam_check_event = threading.Event()
        self._beam_check_thread = None
        self._started = False

    @typechecked
    def register(self, check: BeamlineCondition):
        """
        Register a beamline check.

        Args:
            check (BeamlineCondition): The beamline check to register.
        """
        self._beamline_checks[check.name] = check
        setattr(self, check.name, check)

    def disable_check(self, name: str) -> None:
        """
        Disable a beamline check.

        Args:
            name (str): The name of the beamline check to disable.
        """
        if name not in self._beamline_checks:
            raise ValueError(f"Beamline check {name} not registered.")
        self._beamline_checks[name].enabled = False

    def enable_check(self, name: str) -> None:
        """
        Enable a beamline check.

        Args:
            name (str): The name of the beamline check to enable.
        """
        if name not in self._beamline_checks:
            raise ValueError(f"Beamline check {name} not registered.")
        self._beamline_checks[name]["enabled"] = True

    def disable_all_checks(self) -> None:
        """
        Disable all beamline checks.
        """
        for name in self._beamline_checks:
            self.disable_check(name)

    def enable_all_checks(self) -> None:
        """
        Enable all beamline checks.
        """
        for name in self._beamline_checks:
            self.enable_check(name)

    def _run_beamline_checks(self):
        msgs = []
        for check in self._beamline_checks:
            if not check.enabled:
                continue
            if check.run():
                continue
            msgs.append(check.on_failure_msg())
            self._beam_is_okay = False
        return msgs

    def _check_beam(self):
        while not self._stop_beam_check_event.is_set():
            self._check_msgs = self._run_beamline_checks()

            if not self._beam_is_okay:
                self._stop_beam_check_event.set()
            time.sleep(1)

    def start(self):
        """Start the beamline checks."""
        if self._started:
            return
        self._beam_is_okay = True

        self._beam_check_thread = threading.Thread(target=self._check_beam, daemon=True)
        self._beam_check_thread.start()

    def was_beam_okay(self):
        self._stop_beam_check_event.set()
        self.beam_check_thread.join()
        return self._beam_is_okay

    def _print_beamline_checks(self):
        for msg in self._check_msgs:
            logger.warning(msg)

    def wait_for_beamline_checks(self):
        self._print_beamline_checks()
        if self.send_to_scilog:
            self._send_to_scilog(
                f"Beamline checks failed at {str(datetime.datetime.now())}: {''.join(self._check_msgs)}",
                pen="red",
            )

        while True:
            self._beam_is_okay = True
            self._check_msgs = self._run_beamline_checks()
            if self._beam_is_okay:
                break
            self._print_beamline_checks()
            time.sleep(1)

        if self.send_to_scilog:
            self._send_to_scilog(
                f"Operation resumed at {str(datetime.datetime.now())}.", pen="green"
            )

    def _send_to_scilog(self, msg, pen="red"):
        try:
            msg = self.client.logbook.LogbookMessage()
            msg.add_text(f"<p><mark class='pen-{pen}'><strong>{msg}</strong></mark></p>").add_tag(
                ["BEC", "beam_check"]
            )
            self.client.logbook.send_logbook_message(msg)
        except Exception:
            logger.warning("Failed to send update to SciLog.")


# # a guarded function will upon entering the function check if the beam is okay. If not, it will wait until the beam is okay.
# # if the beam is okay, it will also check if the function call is within another nested guarded function call. If so,
# # it will not wait for the beam to be okay and instead return immediately.
# import inspect


# def bl_check(fcn):
#     """Decorator to perform rpc calls."""

#     @functools.wraps(fcn)
#     def wrapper(self, *args, **kwargs):
#         client = builtins.__dict__.get("bec")
#         bl_checks = client.bl_checks
#         stack = inspect.stack()
#         for frame in stack:
#             if frame.function == "wrapper":
#                 break
#             if frame.function == "bl_check":
#                 return fcn(*args, **kwargs)
#         successful = False
#         while not successful:
#             bl_checks.start_beam_check()

#             res = fcn(self, *args, **kwargs)
#             error_caught = False

#             if bl_checks.was_beam_okay():
#                 successful = True
#             else:
#                 bl_checks.wait_for_beamline_checks()
#         return res

#     return wrapper


# while not successful:
#     try:
#         start_scan_number = bec.queue.next_scan_number
#         for i in range(num_repeats):
#             self._at_each_angle(angle)
#         error_caught = False
#     except AlarmBase as exc:
#         if exc.alarm_type == "TimeoutError":
#             bec.queue.request_queue_reset()
#             time.sleep(2)
#             error_caught = True
#         else:
#             raise exc

#     if self._was_beam_okay() and not error_caught:
#         successful = True
#     else:
#         self._wait_for_beamline_checks()


# """
# With every new bl_check level, the following should be done:
# - Add the new level to the list of levels in the client
# """

from uuid import uuid4

# decorator to add a new bl_check level


class BeamlineCheckError(Exception):
    pass


if __name__ == "__main__":
    import builtins
    import functools
    import inspect
    from collections import deque
    from unittest import mock

    bl_check_levels = deque()

    def bl_check(fcn):
        """Decorator to perform rpc calls."""

        @functools.wraps(fcn)
        def bl_check_wrapper(*args, **kwargs):
            # client = builtins.__dict__.get("bec")
            client = mock.MagicMock()
            bl_checks = client.bl_checks
            chk = {"id": str(uuid4()), "fcn": fcn, "args": args, "kwargs": kwargs}
            bl_check_levels.append(chk)
            nested_call = len(bl_check_levels) > 1
            try:
                if nested_call:
                    # check if the beam was okay so far
                    if not bl_checks.was_beam_okay():
                        raise BeamlineCheckError("Beam is not okay.")
                else:
                    bl_checks.reset()
                successful = False
                while not successful:
                    bl_checks.start_beam_check()
                    try:
                        res = fcn(*args, **kwargs)
                    except BeamlineCheckError:
                        successful = False
                        continue

                    if bl_checks.was_beam_okay():
                        successful = True
                    else:
                        bl_checks.wait_for_beamline_checks()
                return res

            finally:
                bl_check_levels.pop()

        return bl_check_wrapper

    @bl_check
    def func1(input):
        print("func1")
        print(input)

    @bl_check
    def func2():
        func1("hello")
        print("func2")

    func2()
    func1("hello")
    func2()
