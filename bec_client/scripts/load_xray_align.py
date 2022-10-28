def lamni_read_alignment_parameters():
    
    f = open("ptychotomoalign_Ax.txt", "r")
    tomo_fit_xray_eye[0][0] = f.readline()
    f.close()

    f = open("ptychotomoalign_Bx.txt", "r")
    tomo_fit_xray_eye[0][1] = f.readline()
    f.close()

    f = open("ptychotomoalign_Cx.txt", "r")
    tomo_fit_xray_eye[0][2] = f.readline()
    f.close()

    f = open("ptychotomoalign_Ay.txt", "r")
    tomo_fit_xray_eye[1][0] = f.readline()
    f.close()

    f = open("ptychotomoalign_By.txt", "r")
    tomo_fit_xray_eye[1][1] = f.readline()
    f.close()

    f = open("ptychotomoalign_Cy.txt", "r")
    tomo_fit_xray_eye[1][2] = f.readline()
    f.close()

    bk.set_global_var("tomo_fit_xray_eye", tomo_fit_xray_eye)
    # x amp, phase, offset, y amp, phase, offset
    #  0 0    0 1    0 2     1 0    1 1    1 2

    print("New alignment parameters loaded from X-ray eye\n")
    print(f"X Amplitude {tomo_fit_xray_eye[0][0]},
            X Phase {tomo_fit_xray_eye[0][1]}, 
            X Offset {tomo_fit_xray_eye[0][2]},
            Y Amplitude {tomo_fit_xray_eye[1][0]},
            Y Phase {tomo_fit_xray_eye[1][1]},
            Y Offset {tomo_fit_xray_eye[1][2]}")

    return()
