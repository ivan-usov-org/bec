def dscan(motor1, m1_from, m1_to, steps, exp_time, **kwargs):
    return scans.line_scan(
        motor1, m1_from, m1_to, steps=steps, exp_time=exp_time, relative=True, **kwargs
    )


def d2scan(motor1, m1_from, m1_to, motor2, m2_from, m2_to, steps, exp_time, **kwargs):
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
    return scans.line_scan(
        motor1, m1_from, m1_to, steps=steps, exp_time=exp_time, relative=False, **kwargs
    )


def a2scan(motor1, m1_from, m1_to, motor2, m2_from, m2_to, steps, exp_time, **kwargs):
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


def umv(*args):
    return scans.umv(*args, relative=False)


def umvr(*args):
    return scans.umv(*args, relative=True)


def mv(*args):
    return scans.mv(*args, relative=False)


def mvr(*args):
    return scans.mv(*args, relative=True)
