def tomo_scan(subtomo_number):
    import numpy as np

    _tomo_stepsize=10

    if subtomo_number == 1:
        start_angle=0
    elif subtomo_number == 2:
        start_angle=_tomo_stepsize / 8.0 * 4
    elif subtomo_number == 3:
        start_angle=_tomo_stepsize / 8.0 * 2
    elif subtomo_number == 4:
        start_angle=_tomo_stepsize / 8.0 * 6
    elif subtomo_number == 5:
        start_angle=_tomo_stepsize / 8.0 * 1
    elif subtomo_number == 6:
        start_angle=_tomo_stepsize / 8.0 * 5
    elif subtomo_number == 7:
        start_angle=_tomo_stepsize / 8.0 * 3
    elif subtomo_number == 8:
        start_angle=_tomo_stepsize / 8.0 * 7

    #_tomo_shift_angles (potential global variable)
    _tomo_shift_angles=0
    ii_end = start_angle+360
    print (start_angle) 
    for ii in np.linspace(start_angle+_tomo_shift_angles, ii_end, num=360/_tomo_stepsize+1, endpoint=True):
        if ii in range(0,361):
            print (ii)


