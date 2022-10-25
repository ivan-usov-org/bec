import time
from collections import defaultdict

import epics


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
            print("waiting for live view to start..\n")
        fshopen()

        epics_put("XOMNYI-XEYE-ACQDONE:0", 0)

        while epics_get("XOMNYI-XEYE-ACQDONE:0") == 0:
            print("waiting for new frame..\n")
            time.sleep(0.5)

        time.sleep(0.5)
        # stop live view
        epics_put("XOMNYI-XEYE-ACQ:0", 0)
        time.sleep(1)
        # fshclose
        print("got new frame\n")

    def _disable_rt_feedback(self):
        self.device_manager.devices.rtx.controller.feedback_disable()

    def _enable_rt_feedback(self):
        self.device_manager.devices.rtx.controller.feedback_enable_with_reset()

    def _loptics_out(self):
        raise NotImplementedError

    def tomo_rotate(self, val:float):
        umv(self.device_manager.lsamrot, val)

    def get_tomo_angle(self):
        raise NotImplementedError

    def _lfzp_in(self):
        raise NotImplementedError

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
        # TODO prepare output files
        # dname = sprintf("%sptychotomoalign_scannum.txt",_spec_internal_dir())
        # unix(sprintf("rm -f %s",dname))

        # dname = sprintf("%sptychotomoalign_numproj.txt",_spec_internal_dir())
        # unix(sprintf("rm -f %s",dname))

        # #dname = sprintf("%sptychotomoalign_*.txt",_spec_internal_dir())
        # #unix(sprintf("rm -f %s",dname))

        # dname = sprintf("%sxrayeye_alignmentvalue_x*",_spec_internal_dir())
        # unix(sprintf("rm -f %s",dname))

        # dname = sprintf("%sptycho_alignmentvalue_x*",_spec_internal_dir())
        # unix(sprintf("rm -f %s",dname))

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
                    f"Clicked position {k}: x {self.alignment_values[k][0]}, y {self.alignment_values[k][1]}\n"
                )

                if k == 0:  # received center value of FZP
                    self.send_message("please wait ...")
                    # perform movement: FZP out, Sample in
                    self._loptics_out()
                    epics_put("XOMNYI-XEYE-SUBMIT:0", -1)  # disable submit button
                    self.movement_buttons_enabled = False
                    print("Moving sample in, FZP out\n")

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
                        f"Base shift values from movement are x {self.shift_xy[0]}, y {self.shift_xy[1]}\n"
                    )
                    self.shift_xy[0] += (
                        self.alignment_values[0][0] - self.alignment_values[0][1]
                    ) * 1000
                    self.shift_xy[1] += (
                        self.alignment_values[1][1] - self.alignment_values[1][0]
                    ) * 1000
                    print(
                        f"Base shift values from movement and clicked position are x {self.shift_xy[0]}, y {self.shift_xy[1]}\n"
                    )

                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0]/1000, self.shift_xy[1]/1000, self.get_tomo_angle()
                    ).wait()

                    self.send_message("please wait ...")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", -1)  # disable submit button
                    self.movement_buttons_enabled = False
                    time.sleep(1)

                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0]/1000, self.shift_xy[1]/1000, self.get_tomo_angle() 
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
                    self._tomo_rotate((k - 1) * 45 - 45 / 2)
                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0]/1000, self.shift_xy[1]/1000, self.get_tomo_angle()
                    ).wait()
                    self._disable_rt_feedback()
                    self._tomo_rotate((k - 1) * 45)
                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0]/1000, self.shift_xy[1]/1000, self.get_tomo_angle()
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
                    shiftx = shiftx + _xrayeyalignmvx
                    shifty = shifty + _xrayeyalignmvy
                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0]/1000, self.shift_xy[1]/1000, self.get_tomo_angle()
                    ).wait()
                    print(f"Current center horizontal {shiftx} vertical {shifty}\n")
                    epics_put("XOMNYI-XEYE-MVY:0", 0)
                    epics_put("XOMNYI-XEYE-MVX:0", 0)
                    self.update_frame()

            time.sleep(0.2)


# # ----------------------------------------------------------------------
# def _ttl_check_channel_out(channel) '{
#   if ((channel < 1) || (channel > _ttl_out_channel_max)) {
#     printf("TTL: channel must be within the range from 1 to %d. Current value is %.0f.\n",\
#            _ttl_out_channel_max,channel)
#     exit
#   }
#   return (sprintf("X12SA-ES1-TTL:OUT_%02.0f",channel))
# }'


# io.mac
# # ----------------------------------------------------------------------
# def _ttl_out(channel,value) '{
#   global _io_debug
#   local epics_channel

#   # check for valid channel number
#   epics_channel = _ttl_check_channel_out(channel)

#   if ((value != 0) && (value != 1)) {
#     printf("ttl_out: value must be 0 or 1. Current value is %.0f.\n",value)
#     exit
#   }

#   epics_put_stop(sprintf("%s.VAL",epics_channel),value,2.0,"_ttl_out")
#   if (_io_debug) {
#     printf("_ttl_out(%d,%d)\n",channel,value)
#   }
# }'


# shutter.mac
# ----------------------------------------------------------------------
# def fshopen '{
#   _ttl_out(_fsh_ttl_channel,1)
# }'

# # ----------------------------------------------------------------------
# def fshclose '{
#   global _fsh_close_delay_active
#   global _fsh_single_delay_active

#   # ensure that the delayed closing is deactivated
#   epics_put("X12SA-ES1-FSHDELAY:ON","OFF")
#   _fsh_close_delay_active = 0
#   _fsh_single_delay_active = 0

#   # close the fast shutter
#   _ttl_out(_fsh_ttl_channel,0)
# }'

# # ----------------------------------------------------------------------
# def fshon '{
#   global _fsh_is_on

#   if (_fsh_is_on) {
#     printf("The fast shutter is already enabled.\n")
#   } else {
#     printf("Enabling the fast shutter.\n")
#   }

#   _fsh_is_on = 1
#   ttl_out_auto _fsh_ttl_channel 1
#   if (_io_wait_time < _fsh_wait_time_sec) {
#     printf("increasing the IO wait time from %.3f to %.3f seconds:\n",\
#            _io_wait_time,_fsh_wait_time_sec)
#     io_wait _fsh_wait_time_sec
#   }
# }'
