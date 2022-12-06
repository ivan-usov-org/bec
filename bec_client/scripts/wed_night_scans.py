import threading
from bec_utils.logbook_connector import LogbookMessage
import builtins
import time
from bec_utils import bec_logger
from bec_client.plugins.cSAXS import epics_put, epics_get
import numpy as np

logger = bec_logger.logger


def cm():
    umv(dev.ppx, 0)
    # current_energy = 7.2459
    current_energy = dev.mokev.read()["mokev"]["value"]
    umv(dev.ppth, 3.637495 * current_energy - 16.649682)
    bec.metadata.update({"polarization": 1})


def cp():
    umv(dev.ppx, 0)
    # current_energy = 7.2459
    current_energy = dev.mokev.read()["mokev"]["value"]
    umv(dev.ppth, 3.646599 * current_energy - 16.682671)
    bec.metadata.update({"polarization": 2})


def pp_out():
    umv(dev.ppx, 50)
    bec.metadata.update({"polarization": 0})


class BeamlineChecks:
    def __init__(self, client):
        self.client = client
        self.check_shutter = True
        self.check_light_available = True
        self.check_fofb = True

    def _run_beamline_checks(self):
        msgs = []
        dev = builtins.__dict__.get("dev")
        try:
            if self.check_shutter:
                shutter_val = dev.x12sa_es1_shutter_status.read(cached=True)
                if shutter_val["value"].lower() != "open":
                    self._beam_is_okay = False
                    msgs.append("Check beam failed: Shutter is closed.")
            if self.check_light_available:
                machine_status = dev.sls_machine_status.read(cached=True)
                if machine_status["value"] not in ["Light Available", "Light-Available"]:
                    self._beam_is_okay = False
                    msgs.append("Check beam failed: Light not available.")
            if self.check_fofb:
                fast_orbit_feedback = dev.sls_fast_orbit_feedback.read(cached=True)
                if fast_orbit_feedback["value"] != "running":
                    self._beam_is_okay = False
                    msgs.append("Check beam failed: Fast orbit feedback is not running.")
        except Exception:
            logger.warning("Failed to check beam.")
        return msgs

    def _check_beam(self):
        while not self._stop_beam_check_event.is_set():
            self._check_msgs = self._run_beamline_checks()

            if not self._beam_is_okay:
                self._stop_beam_check_event.set()
            time.sleep(1)

    def _start_beam_check(self):
        self._beam_is_okay = True
        self._stop_beam_check_event = threading.Event()

        self.beam_check_thread = threading.Thread(target=self._check_beam, daemon=True)
        self.beam_check_thread.start()

    def _was_beam_okay(self):
        self._stop_beam_check_event.set()
        self.beam_check_thread.join()
        return self._beam_is_okay

    def _print_beamline_checks(self):
        for msg in self._check_msgs:
            logger.warning(msg)

    def _wait_for_beamline_checks(self):
        self._print_beamline_checks()
        try:
            msg = LogbookMessage(self.client.logbook)
            msg.add_text(
                f"<p><mark class='pen-red'><strong>Beamline checks failed at {str(datetime.datetime.now())}: {''.join(self._check_msgs)}</strong></mark></p>"
            ).add_tag(["BEC", "beam_check"])
            self.client.logbook.send_logbook_message(msg)
        except Exception:
            logger.warning("Failed to send update to SciLog.")

        while True:
            self._beam_is_okay = True
            self._check_msgs = self._run_beamline_checks()
            if self._beam_is_okay:
                break
            self._print_beamline_checks()
            time.sleep(1)

        try:
            msg = LogbookMessage(self.client.logbook)
            msg.add_text(
                f"<p><mark class='pen-green'><strong>Operation resumed at {str(datetime.datetime.now())}.</strong></mark></p>"
            ).add_tag(["BEC", "beam_check"])
            self.client.logbook.send_logbook_message(msg)
        except Exception:
            logger.warning("Failed to send update to SciLog.")


def test_2d(lamni):
    """overnight scan on wed"""
    beam_checks = BeamlineChecks(bec)
    for step in [0.7]:
        lamni.tomo_shellstep = step
        for angle in [180, 90, 0]:
            cp()
            for ii in range(10):
                successful = False
                while not successful:
                    beam_checks._start_beam_check()
                    lamni.tomo_scan_projection(angle)
                    if beam_checks._was_beam_okay():
                        successful = True
                    else:
                        beam_checks._wait_for_beamline_checks()
                lamni.tomo_reconstruct()

            cm()
            for ii in range(10):
                successful = False
                while not successful:
                    beam_checks._start_beam_check()
                    lamni.tomo_scan_projection(angle)
                    if beam_checks._was_beam_okay():
                        successful = True
                    else:
                        beam_checks._wait_for_beamline_checks()
                lamni.tomo_reconstruct()


def temp_scan_2d(lamni, angle):
    """test 2D with input angle"""
    # angle = 180
    beam_checks = BeamlineChecks(bec)
    cp()
    for ii in range(5):
        successful = False
        while not successful:
            beam_checks._start_beam_check()
            lamni.tomo_scan_projection(angle)
            if beam_checks._was_beam_okay():
                successful = True
            else:
                beam_checks._wait_for_beamline_checks()
        lamni.tomo_reconstruct()

    cm()
    for ii in range(5):
        successful = False
        while not successful:
            beam_checks._start_beam_check()
            lamni.tomo_scan_projection(angle)
            if beam_checks._was_beam_okay():
                successful = True
            else:
                beam_checks._wait_for_beamline_checks()
        lamni.tomo_reconstruct()


# def temperature_scan_2d(lamni):
#     """ test 2D with different temperatures - initial try, NOT tested """
#     angle = 180
#     beam_checks = BeamlineChecks(bec)
#     for temps in [0, 90, 180, 270]:
#     cp()
#     for ii in range(10):
#         successful = False
#         while not successful:
#             beam_checks._start_beam_check()
#             lamni.tomo_scan_projection(angle)
#             if beam_checks._was_beam_okay():
#                 successful = True
#             else:
#                 beam_checks._wait_for_beamline_checks()
#         lamni.tomo_reconstruct()

#     cm()
#     for ii in range(10):
#         successful = False
#         while not successful:
#             beam_checks._start_beam_check()
#             lamni.tomo_scan_projection(angle)
#             if beam_checks._was_beam_okay():
#                 successful = True
#             else:
#                 beam_checks._wait_for_beamline_checks()
#         lamni.tomo_reconstruct()


def go_to_temp(target_val, step_size=10, tolerance=0.1):
    if target_val > 250:
        raise ValueError("Cannot go beyond 250 mA.")
    val = epics_get("X12SA-ES1-DOUBLE-05")
    current_temp_start = dev.sample_temp.read()["sample_temp"]["value"]
    if current_temp_start > target_val:
        step_size *= -1
    while True:
        val += step_size
        epics_put("X12SA-ES1-DOUBLE-05", val)
        time.sleep(0.5)
        current_temp = dev.sample_temp.read()["sample_temp"]["value"]
        print(f"Sample resistance: {current_temp:.4f}, current: {val:.4f}")
        if (
            np.isclose(current_temp, target_val, atol=tolerance)
            or (step_size > 0 and current_temp > target_val)
            or (step_size < 0 and current_temp < target_val)
        ):
            break
        if val <= 0:
            break
    bec.metadata.update({"sample_current": val})


def temperature_scan_3d(lamni):
    """select temperatures, all angles, 2 projections at each angle"""

    for resistance in [167, 175, 180]:  # TODO: update with select temperature/resistance
        go_to_temp(resistance)
        try:
            bec.logbook.send_message(
                f"First scan number: {bec.queue.next_scan_number}, Sample resistance: {resistance}"
            )
        except Exception:
            print("Failed to write to scilog.")

        lamni.tomo_scan()


def lunchtime_scan(lamni):
    temp_scan_2d(lamni, 0)
    temp_scan_2d(lamni, 90)
    temp_scan_2d(lamni, 180)
    # lamni.tomo_scan()


def go_to_mark(mark_number: float):
    current_mark = epics_get("X12SA-ES1-DOUBLE-03")
    logger.info(f"Going from mark {current_mark} to mark {mark_number}.")
    print(f"Going from mark {current_mark} to mark {mark_number}.")
    epics_put("X12SA-ES1-DOUBLE-04", mark_number)
    while not np.isclose(epics_get("X12SA-ES1-DOUBLE-03"), mark_number, atol=0.001):
        print(f"Waiting until mark {mark_number} is reached.")
        time.sleep(1)
    print(f"We are now at mark {mark_number}.")
    bec.metadata.update({"mark": mark_number})


def spectral_scan(lamni, start, stop, angle, step_size=0.01):
    bec.logbook.send_message(
        f"Spectral scan spectral_scan(lamni,{start}, {stop}, {angle}, step_size={step_size})"
    )
    go_to_mark(0)
    num_pos = round((stop - start) / step_size)
    for mark_pos in np.linspace(start, num_pos * step_size + start, num_pos, endpoint=False):
        go_to_mark(mark_pos)
        bec.logbook.send_message(f"Energy = {dev.mokev.read()['mokev']['value']:.04f}")
        cp()
        lamni.tomo_scan_projection(angle)
        lamni.tomo_reconstruct()
        cm()
        lamni.tomo_scan_projection(angle)
        lamni.tomo_reconstruct()


def temperature_scan_2d(lamni):
    """select temperatures, all angles, 2 projections at each angle"""

    for resistance in [
        168,
        174,
        181,
        200,
        208,
        216,
        224,
        230,
        236.6,
        243,
        247,
    ]:  # TODO: update with select temperature/resistance
        go_to_temp(resistance)
        try:
            bec.logbook.send_message(
                f"First scan number: {bec.queue.next_scan_number}, Sample resistance: {resistance}"
            )
        except Exception:
            print("Failed to write to scilog.")
        temp_scan_2d(lamni, 90)


def spectral_scan_many(lamni, start, stop, angle, step_size=0.01, num_ave=1):
    bec.logbook.send_message(
        f"Spectral scan spectral_scan(lamni,{start}, {stop}, {angle}, step_size={step_size})"
    )
    go_to_mark(0)
    num_pos = round((stop - start) / step_size)
    for mark_pos in np.linspace(start, num_pos * step_size + start, num_pos, endpoint=False):
        go_to_mark(mark_pos)
        bec.logbook.send_message(f"Energy = {dev.mokev.read()['mokev']['value']:.04f}")
        for ii in range(num_ave):
            cp()
            lamni.tomo_scan_projection(angle)
            lamni.tomo_reconstruct()
            cm()
            lamni.tomo_scan_projection(angle)
            lamni.tomo_reconstruct()
