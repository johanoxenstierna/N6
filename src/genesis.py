
import random
import P as P
import numpy as np

import P

# from sh_info import shInfoAbstract, _0_info
from sh_info import _6_info

def init_infos():
    '''Creates instance of each info and stores in dict'''
    infos = {}

    top_point6 = [640, 420]

    EXPL_F = 10  # 1300

    # pulse_6 = [10, 11, 130]
    # pulse_6 = [EXPL_F, EXPL_F + 40, EXPL_F + 60]
    # pulse_6 = list(np.array([10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 70, 80, 90, 120, 150, 200, 205, 210, 215, 220, 225], dtype=int))
    # pulse_6 = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 140, 141, 142, 143, 144, 145, 146]

    p6 = []
    bat_is = [10, 260]
    for bi in bat_is:
        pulse = list(range(bi, bi + P.NUM_FS))
        p6.extend(pulse)
        df = 5

    # pulse_6 = list(np.random.choice(range(10, 200), size=100, replace=False))

    p6.sort()


    if '6' in P.SHS_TO_SHOW:  # EXPL
        _6 = _6_info.Sh_6_info(p6)
        infos[_6.id] = _6

    return infos