import numpy as np


def sub_tomo_scan(subtomo_number, start_angle=None, tomo_stepsize=10.0):

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
            lamni.tomo_scan_projection(angle)


def tomo_scan():
    for ii in range(8):
        sub_tomo_scan(ii + 1)
