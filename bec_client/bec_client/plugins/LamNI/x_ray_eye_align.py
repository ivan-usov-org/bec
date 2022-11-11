import builtins
import os
import time
from collections import defaultdict

import epics
import numpy as np
from bec_utils import bec_logger

logger = bec_logger.logger


def epics_put(channel, value):
    epics.caput(channel, value)


def epics_get(channel):
    return epics.caget(channel)


def fshopen():
    pass


class XrayEyeAlign:
    # pixel calibration, multiply to get mm
    # PIXEL_CALIBRATION = 0.2/209 #.2 with binning
    PIXEL_CALIBRATION = 0.2 / 218  # .2 with binning

    def __init__(self, client) -> None:
        self.client = client
        self.device_manager = client.device_manager
        self.scans = client.scans
        self.xeye = self.device_manager.devices.xeye
        self.alignment_values = defaultdict(list)
        self.shift_xy = [0, 0]
        self._xray_fov_xy = [0, 0]

    def save_frame(self):
        epics_put("XOMNYI-XEYE-SAVFRAME:0", 1)

    def update_frame(self):
        epics_put("XOMNYI-XEYE-ACQDONE:0", 0)
        # start live
        epics_put("XOMNYI-XEYE-ACQ:0", 1)
        # wait for start live
        while epics_get("XOMNYI-XEYE-ACQDONE:0") == 0:
            time.sleep(0.5)
            print("waiting for live view to start...")
        fshopen()

        epics_put("XOMNYI-XEYE-ACQDONE:0", 0)

        while epics_get("XOMNYI-XEYE-ACQDONE:0") == 0:
            print("waiting for new frame...")
            time.sleep(0.5)

        time.sleep(0.5)
        # stop live view
        epics_put("XOMNYI-XEYE-ACQ:0", 0)
        time.sleep(1)
        # fshclose
        print("got new frame")

    def _disable_rt_feedback(self):
        self.device_manager.devices.rtx.controller.feedback_disable()

    def _enable_rt_feedback(self):
        self.device_manager.devices.rtx.controller.feedback_enable_with_reset()

    def _loptics_out(self):
        # raise NotImplementedError
        pass

    def tomo_rotate(self, val: float):
        umv(self.device_manager.devices.lsamrot, val)

    def get_tomo_angle(self):
        return self.device_manager.devices.lsamrot.readback.read()["lsamrot"]["value"]

    def _lfzp_in(self):
        # raise NotImplementedError
        pass

    def update_fov(self, k: int):
        self._xray_fov_xy[0] = max(epics_get(f"XOMNYI-XEYE-XWIDTH_X:{k}"), self._xray_fov_xy[0])
        self._xray_fov_xy[1] = max(0, self._xray_fov_xy[0])

    @property
    def movement_buttons_enabled(self):
        return [epics_get("XOMNYI-XEYE-ENAMVX:0"), epics_get("XOMNYI-XEYE-ENAMVY:0")]

    @movement_buttons_enabled.setter
    def movement_buttons_enabled(self, enabled: bool):
        enabled = int(enabled)
        epics_put("XOMNYI-XEYE-ENAMVX:0", enabled)
        epics_put("XOMNYI-XEYE-ENAMVY:0", enabled)

    def send_message(self, msg: str):
        epics_put("XOMNYI-XEYE-MESSAGE:0.DESC", msg)

    def align(self):
        # this makes sure we are in a defined state
        self._disable_rt_feedback()

        epics_put("XOMNYI-XEYE-PIXELSIZE:0", self.PIXEL_CALIBRATION)

        self._enable_rt_feedback()

        # initialize
        # disable movement buttons
        self.movement_buttons_enabled = False

        epics_put("XOMNYI-XEYE-ACQ:0", 0)
        self.send_message("please wait...")

        # put sample name
        epics_put("XOMNYI-XEYE-SAMPLENAME:0.DESC", "Let us LAMNI...")

        # first step
        self._disable_rt_feedback()
        k = 0

        # move zone plate in, eye in to get beam position
        self._lfzp_in()

        self.update_frame()

        # enable submit buttons
        self.movement_buttons_enabled = False
        epics_put("XOMNYI-XEYE-SUBMIT:0", 0)
        epics_put("XOMNYI-XEYE-STEP:0", 0)
        self.send_message("Submit center value of FZP.")

        while True:
            if epics_get("XOMNYI-XEYE-SUBMIT:0") == 1:
                val_x = epics_get(f"XOMNYI-XEYE-XVAL_X:{k}") * self.PIXEL_CALIBRATION  # in mm
                val_y = epics_get(f"XOMNYI-XEYE-YVAL_Y:{k}") * self.PIXEL_CALIBRATION  # in mm
                self.alignment_values[k] = [val_x, val_y]
                print(
                    f"Clicked position {k}: x {self.alignment_values[k][0]}, y {self.alignment_values[k][1]}"
                )

                if k == 0:  # received center value of FZP
                    self.send_message("please wait ...")
                    # perform movement: FZP out, Sample in
                    self._loptics_out()
                    epics_put("XOMNYI-XEYE-SUBMIT:0", -1)  # disable submit button
                    self.movement_buttons_enabled = False
                    print("Moving sample in, FZP out")

                    self._disable_rt_feedback()
                    time.sleep(0.3)
                    self._enable_rt_feedback()
                    time.sleep(0.3)

                    # zero is now at the center
                    self.update_frame()
                    self.send_message("Go and find the sample")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", 0)
                    self.movement_buttons_enabled = True

                elif (
                    k == 1
                ):  # received sample center value at samroy 0 ie the final base shift values
                    print(
                        f"Base shift values from movement are x {self.shift_xy[0]}, y {self.shift_xy[1]}"
                    )
                    self.shift_xy[0] += (
                        self.alignment_values[0][0] - self.alignment_values[1][0]
                    ) * 1000
                    self.shift_xy[1] += (
                        self.alignment_values[1][1] - self.alignment_values[0][1]
                    ) * 1000
                    print(
                        f"Base shift values from movement and clicked position are x {self.shift_xy[0]}, y {self.shift_xy[1]}"
                    )

                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0] / 1000, self.shift_xy[1] / 1000, self.get_tomo_angle()
                    ).wait()

                    self.send_message("please wait ...")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", -1)  # disable submit button
                    self.movement_buttons_enabled = False
                    time.sleep(1)

                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0] / 1000, self.shift_xy[1] / 1000, self.get_tomo_angle()
                    ).wait()

                    epics_put("XOMNYI-XEYE-ANGLE:0", self.get_tomo_angle())
                    self.update_frame()
                    self.send_message("Submit sample center and FOV (0 deg)")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", 0)
                    self.update_fov(k)

                elif 1 < k < 10:  # received sample center value at samroy 0 ... 315
                    self.send_message("please wait ...")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", -1)  # disable submit button

                    # we swtich feedback off before rotating to not have it on and off again later for smooth operation
                    self._disable_rt_feedback()
                    self.tomo_rotate((k - 1) * 45 - 45 / 2)
                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0] / 1000, self.shift_xy[1] / 1000, self.get_tomo_angle()
                    ).wait()
                    self._disable_rt_feedback()
                    self.tomo_rotate((k - 1) * 45)
                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0] / 1000, self.shift_xy[1] / 1000, self.get_tomo_angle()
                    ).wait()

                    epics_put("XOMNYI-XEYE-ANGLE:0", self.get_tomo_angle())
                    self.update_frame()
                    self.send_message("Submit sample center")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", 0)
                    epics_put("XOMNYI-XEYE-ENAMVX:0", 1)
                    self.update_fov(k)

                elif k == 10:  # received sample center value at samroy 270 and done
                    self.send_message("done...")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", -1)  # disable submit button
                    self.movement_buttons_enabled = False
                    self.update_fov(k)
                    break

                k += 1
                epics_put("XOMNYI-XEYE-STEP:0", k)
            if k < 2:
                # allow movements, store movements to calculate center
                _xrayeyalignmvx = epics_get("XOMNYI-XEYE-MVX:0")
                _xrayeyalignmvy = epics_get("XOMNYI-XEYE-MVY:0")
                if _xrayeyalignmvx != 0 or _xrayeyalignmvy != 0:
                    self.shift_xy[0] = self.shift_xy[0] + _xrayeyalignmvx
                    self.shift_xy[1] = self.shift_xy[1] + _xrayeyalignmvy
                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0] / 1000, self.shift_xy[1] / 1000, self.get_tomo_angle()
                    ).wait()
                    print(
                        f"Current center horizontal {self.shift_xy[0]} vertical {self.shift_xy[1]}"
                    )
                    epics_put("XOMNYI-XEYE-MVY:0", 0)
                    epics_put("XOMNYI-XEYE-MVX:0", 0)
                    self.update_frame()

            time.sleep(0.2)

        self.write_output()
        fovx = self._xray_fov_xy[0] * self.PIXEL_CALIBRATION * 1000 / 2
        fovy = self._xray_fov_xy[1] * self.PIXEL_CALIBRATION * 1000 / 2
        print(
            f"The largest field of view from the xrayeyealign was \nfovx = {fovx:.0f} microns, fovy = {fovy:.0f} microns"
        )
        print("Use matlab routine to fit the current alignment...")

        print(
            f"This additional shift is applied to the base shift values\n which are x {self.shift_xy[0]}, y {self.shift_xy[1]}"
        )

        self._disable_rt_feedback()

        self.tomo_rotate(0)

        print("\n\nNEXT LOAD ALIGNMENT PARAMETERS\nby running lamni_read_alignment_parameters\n")

        self.client.set_global_var("tomo_fov_offset", self.shift_xy)

    def write_output(self):
        with open(
            os.path.expanduser("~/Data10/specES1/internal/xrayeye_alignmentvalues"), "w"
        ) as alignment_values_file:
            alignment_values_file.write(f"angle\thorizontal\tvertical\n")
            for k in range(2, 11):
                fovx_offset = (self.alignment_values[0][0] - self.alignment_values[k][0]) * 1000
                fovy_offset = (self.alignment_values[k][1] - self.alignment_values[0][1]) * 1000
                print(
                    f"Writing to file new alignment: number {k}, value x {fovx_offset}, y {fovy_offset}"
                )
                alignment_values_file.write(f"{(k-2)*45}\t{fovx_offset}\t{fovy_offset}\n")

    def read_alignment_parameters(self, dir_path="~/Data10/specES1/internal/"):
        tomo_fit_xray_eye = np.zeros((2, 3))
        with open(os.path.join(dir_path, "ptychotomoalign_Ax.txt"), "r") as file:
            tomo_fit_xray_eye[0][0] = file.readline()

        with open(os.path.join(dir_path, "ptychotomoalign_Bx.txt"), "r") as file:
            tomo_fit_xray_eye[0][1] = file.readline()

        with open(os.path.join(dir_path, "ptychotomoalign_Cx.txt"), "r") as file:
            tomo_fit_xray_eye[0][2] = file.readline()

        with open(os.path.join(dir_path, "ptychotomoalign_Ay.txt"), "r") as file:
            tomo_fit_xray_eye[1][0] = file.readline()

        with open(os.path.join(dir_path, "ptychotomoalign_By.txt"), "r") as file:
            tomo_fit_xray_eye[1][1] = file.readline()

        with open(os.path.join(dir_path, "ptychotomoalign_Cy.txt"), "r") as file:
            tomo_fit_xray_eye[1][2] = file.readline()

        self.client.set_global_var("tomo_fit_xray_eye", tomo_fit_xray_eye.tolist())
        # x amp, phase, offset, y amp, phase, offset
        #  0 0    0 1    0 2     1 0    1 1    1 2

        print("New alignment parameters loaded from X-ray eye")
        print(
            f"X Amplitude {tomo_fit_xray_eye[0][0]},"
            f"X Phase {tomo_fit_xray_eye[0][1]}, "
            f"X Offset {tomo_fit_xray_eye[0][2]},"
            f"Y Amplitude {tomo_fit_xray_eye[1][0]},"
            f"Y Phase {tomo_fit_xray_eye[1][1]},"
            f"Y Offset {tomo_fit_xray_eye[1][2]}"
        )


class LamNI:
    def __init__(self, client):
        self.client = client
        self.align = XrayEyeAlign(client)
        self.corr_pos_x = []
        self.corr_pos_y = []
        self.corr_angle = []

    @property
    def tomo_fovx_offset(self):
        val = self.client.get_global_var("tomo_fov_offset")
        if val is None:
            return 0.0
        return val[0] / 1000

    @tomo_fovx_offset.setter
    def tomo_fovx_offset(self, val: float):
        self.client.set_global_var("tomo_fov_offset", val)

    @property
    def tomo_fovy_offset(self):
        val = self.client.get_global_var("tomo_fov_offset")
        if val is None:
            return 0.0
        return val[1] / 1000

    @tomo_fovy_offset.setter
    def tomo_fovy_offset(self, val: float):
        self.client.set_global_var("tomo_fov_offset", val)

    @property
    def tomo_shellstep(self):
        val = self.client.get_global_var("tomo_shellstep")
        if val is None:
            return 1
        return val

    @tomo_shellstep.setter
    def tomo_shellstep(self, val: float):
        self.client.set_global_var("tomo_shellstep", val)

    @property
    def tomo_circfov(self):
        val = self.client.get_global_var("tomo_circfov")
        if val is None:
            return 0.0
        return val

    @tomo_circfov.setter
    def tomo_circfov(self, val: float):
        self.client.set_global_var("tomo_circfov", val)

    @property
    def tomo_countingtime(self):
        val = self.client.get_global_var("tomo_countingtime")
        if val is None:
            return 0.0
        return val

    @tomo_countingtime.setter
    def tomo_countingtime(self, val: float):
        self.client.set_global_var("tomo_countingtime", val)

    @property
    def manual_shift_x(self):
        val = self.client.get_global_var("manual_shift_x")
        if val is None:
            return 0.0
        return val

    @manual_shift_x.setter
    def manual_shift_x(self, val: float):
        self.client.set_global_var("manual_shift_x", val)

    @property
    def manual_shift_y(self):
        val = self.client.get_global_var("manual_shift_y")
        if val is None:
            return 0.0
        return val

    @manual_shift_y.setter
    def manual_shift_y(self, val: float):
        self.client.set_global_var("manual_shift_y", val)

    @property
    def lamni_piezo_range(self):
        val = self.client.get_global_var("lamni_piezo_range")
        if val is None:
            return 0.0
        return val

    @lamni_piezo_range.setter
    def lamni_piezo_range(self, val: float):
        self.client.set_global_var("lamni_piezo_range", val)

    def tomo_scan_projection(self, angle: float):
        scans = builtins.__dict__.get("scans")
        additional_correction = self.compute_additional_correction(angle)
        correction_xeye_mu = self.lamni_compute_additional_correction_xeye_mu(angle)
        logger.info(
            f"scans.lamni_fermat_scan(fov_size=[20,20], step={self.tomo_shellstep}, stitch_x={0}, stitch_y={0}, stitch_overlap={1},"
            f"center_x={self.tomo_fovx_offset}, center_y={self.tomo_fovy_offset}, "
            f"shift_x={self.manual_shift_x+correction_xeye_mu[0]-additional_correction[0]}, "
            f"shift_y={self.manual_shift_y+correction_xeye_mu[1]-additional_correction[1]}, "
            f"fov_circular={self.tomo_circfov}, angle={angle}, scan_type='fly')"
        )
        return scans.lamni_fermat_scan(
            fov_size=[20, 20],
            step=self.tomo_shellstep,
            stitch_x=0,
            stitch_y=0,
            stitch_overlap=1,
            center_x=self.tomo_fovx_offset,
            center_y=self.tomo_fovy_offset,
            shift_x=(self.manual_shift_x + correction_xeye_mu[0] - additional_correction[0]),
            shift_y=(self.manual_shift_y + correction_xeye_mu[1] - additional_correction[1]),
            fov_circular=self.tomo_circfov,
            angle=angle,
            scan_type="fly",
        )

    def lamni_compute_additional_correction_xeye_mu(self, angle):
        import math

        tomo_fit_xray_eye = self.client.get_global_var("tomo_fit_xray_eye")
        if tomo_fit_xray_eye is None:
            print("Not applying any additional correction. No x-ray eye data available.\n")
            return (0, 0)

        # x amp, phase, offset, y amp, phase, offset
        #  0 0    0 1    0 2     1 0    1 1    1 2
        correction_x = (
            tomo_fit_xray_eye[0][0] * math.sin(math.radians(angle) + tomo_fit_xray_eye[0][1])
            + tomo_fit_xray_eye[0][2]
        ) / 1000
        correction_y = (
            tomo_fit_xray_eye[1][0] * math.sin(math.radians(angle) + tomo_fit_xray_eye[1][1])
            + tomo_fit_xray_eye[1][2]
        ) / 1000

        print(f"Xeye correction x {correction_x}, y {correction_y} for angle {angle}\n")
        return (correction_x, correction_y)

    def compute_additional_correction(self, angle):
        import math

        if not self.corr_pos_x:
            print("Not applying any additional correction. No data available.\n")
            return (0, 0)

        # find index of closest angle
        for j in range(len(self.corr_pos_x)):
            newangledelta = math.fabs(self.corr_angle[j] - angle)
            if j == 0:
                angledelta = newangledelta
                additional_correction_shift_x = self.corr_pos_x[j]
                additional_correction_shift_y = self.corr_pos_y[j]
                continue

            if newangledelta < angledelta:
                additional_correction_shift_x = self.corr_pos_x[j]
                additional_correction_shift_y = self.corr_pos_y[j]
                angledelta = newangledelta

        if additional_correction_shift_x == 0 and angle < self.corr_angle[0]:
            additional_correction_shift_x = self.corr_pos_x[0]
            additional_correction_shift_y = self.corr_pos_y[0]

        if additional_correction_shift_x == 0 and angle > self.corr_angle[-1]:
            additional_correction_shift_x = self.corr_pos_x[-1]
            additional_correction_shift_y = self.corr_pos_y[-1]
        logger.info(
            f"Additional correction shifts: {additional_correction_shift_x} {additional_correction_shift_y}"
        )
        return (additional_correction_shift_x, additional_correction_shift_y)

    def lamni_read_additional_correction(self, correction_file: str):

        with open(correction_file, "r") as f:
            num_elements = f.readline()
            int_num_elements = int(num_elements.split(" ")[2])
            print(int_num_elements)
            corr_pos_x = []
            corr_pos_y = []
            corr_angle = []
            for j in range(0, int_num_elements * 3):
                line = f.readline()
                value = line.split(" ")[2]
                name = line.split(" ")[0].split("[")[0]
                if name == "corr_pos_x":
                    corr_pos_x.append(float(value) / 1000)
                elif name == "corr_pos_y":
                    corr_pos_y.append(float(value) / 1000)
                elif name == "corr_angle":
                    corr_angle.append(float(value))
        self.corr_pos_x = corr_pos_x
        self.corr_pos_y = corr_pos_y
        self.corr_angle = corr_angle
        return

    def sub_tomo_scan(self, subtomo_number, start_angle=None, tomo_stepsize=10.0):

        if start_angle is None:
            if subtomo_number == 1:
                start_angle = 0
            elif subtomo_number == 2:
                start_angle = tomo_stepsize / 8.0 * 4
            elif subtomo_number == 3:
                start_angle = tomo_stepsize / 8.0 * 2
            elif subtomo_number == 4:
                start_angle = tomo_stepsize / 8.0 * 6
            elif subtomo_number == 5:
                start_angle = tomo_stepsize / 8.0 * 1
            elif subtomo_number == 6:
                start_angle = tomo_stepsize / 8.0 * 5
            elif subtomo_number == 7:
                start_angle = tomo_stepsize / 8.0 * 3
            elif subtomo_number == 8:
                start_angle = tomo_stepsize / 8.0 * 7

        # _tomo_shift_angles (potential global variable)
        _tomo_shift_angles = 0
        angle_end = start_angle + 360
        for angle in np.linspace(
            start_angle + _tomo_shift_angles, angle_end, num=360 / tomo_stepsize + 1, endpoint=True
        ):
            if 0 <= angle < 360.05:
                print(f"Starting LamNI scan for angle {angle}")
                self.tomo_scan_projection(angle)

    def tomo_scan(self):
        for ii in range(8):
            self.sub_tomo_scan(ii + 1)
