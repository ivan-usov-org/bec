def tomo_scan_projection(angle):
    _tomo_fovx_offset = get_global_var("_tomo_fovx_offset")
    _tomo_fovy_offset = get_global_var("_tomo_fovy_offset")

    _tomo_shellstep = get_global_var("_tomo_shellstep")
    _tomo_circfov = get_global_var("_tomo_circfov")
    _tomo_countingtime = get_global_var("_tomo_countingtime")

	_manual_shift_x = get_global_var("_manual_shift_x")
	_manual_shift_y = get_global_var("_manual_shift_y")

	#global _lamni_stitch
	#global _lamni_stitched
	_lamni_piezo_range = get_global_var("_lamni_piezo_range")
	
 	print("lamni_scan _tomo_shellstep _tomo_countingtime 0 0 _tomo_fovx_offset _tomo_fovy_offset _manual_shift_x+_lamni_compute_additional_correction_xeye_mu_x(_angle_for_xeye_correction)-additional_correction_shift_x-additional_correction2_shift_x _manual_shift_y+_lamni_compute_additional_correction_xeye_mu_y(_angle_for_xeye_correction)-additional_correction_shift_y-additional_correction2_shift_y _tomo_circfov _projection_rotate_angle \n")

def _lamni_compute_additional_correction_xeye_mu(angle):
    import math


    tomo_fit_xray_eye = get_global_var("tomo_fit_xray_eye")
    # x amp, phase, offset, y amp, phase, offset
    #  0 0    0 1    0 2     1 0    1 1    1 2  
    correction_x = tomo_fit_xray_eye[0][0] * math.sin(math.radians(angle) + tomo_fit_xray_eye[0][1]) + tomo_fit_xray_eye[0][2]
    correction_y = tomo_fit_xray_eye[1][0] * math.sin(math.radians(angle) + tomo_fit_xray_eye[1][1]) + tomo_fit_xray_eye[1][2]

    print(f"Xeye correction x {correction_x}, y {correction_y} for angle {angle}\n")
    return(correction_x, correction_y)



def isNaN(num):
    if float('-inf') < float(num) < float('inf'):
        return False
    else:
        return True


def compute_additional_correction(angle):
    import math

    additional_correction_shift = get_global_var("additional_correction_shift")
    # [0][] x , [1][] y, [2][] angle, [3][0] number of elements

    if isNaN(additional_correction_shift):
        print("Not applying any additional correction. No data available.\n")
        additional_correction_shift_x = 0
        additional_correction_shift_y = 0
    else:
        #find index of closest angle
        for j in range(0,additional_correction_shift[3][0]):
            newangledelta=math.fabs(additional_correction_shift[2][j]-angle)
            if j == 0:
                angledelta=newangledelta
                additional_correction_shift_x=additional_correction_shift[0][j]
                additional_correction_shift_y=additional_correction_shift[1][j]
            if (newangledelta < angledelta):
                additional_correction_shift_x=additional_correction_shift[0][j]
                additional_correction_shift_y=additional_correction_shift[1][j]
                angledelta=newangledelta

        if additional_correction_shift_x==0 and angle<additional_correction_shift[2][0]:
            additional_correction_shift_x=additional_correction_shift[0][0]
            additional_correction_shift_y=additional_correction_shift[1][0]
                
        if (additional_correction_shift_x==0 and angle>additional_correction_shift[2][additional_correction_shift[3][0]-1]):
            additional_correction_shift_x=additional_correction_shift[0][corr_elements-1]
            additional_correction_shift_y=additional_correction_shift[1][corr_elements-1]

    return(additional_correction_shift_x,additional_correction_shift_y)


