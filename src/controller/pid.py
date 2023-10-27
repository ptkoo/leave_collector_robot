def pid_forward(l: int, r: int, Max_speed: int, p: float, i: float, d: float) -> [int, int]:

    pid = p + i + d

    L_speed = (l) + pid
    R_speed = (r) - pid

    L_speed = abs(L_speed) if abs(L_speed) <= Max_speed else Max_speed
    L_speed = L_speed if L_speed > 0 else 0

    R_speed = abs(R_speed) if abs(R_speed) <= Max_speed else Max_speed
    R_speed = R_speed if R_speed > 0 else 0

    return L_speed, R_speed

