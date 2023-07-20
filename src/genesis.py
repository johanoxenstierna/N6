
import random
import P as P
import numpy as np

import P

# from sh_info import shInfoAbstract, _0_info
from sh_info import _0_info, _1_info, _2_info, _3_info, _4_info, _5_info, _6_info, _7_info, _8_info, _9_info

def init_infos():
    '''Creates instance of each info and stores in dict'''
    infos = {}

    top_point6 = [640, 420]

    EXPL_F = 10  # 1300

    pulse_6 = [EXPL_F]
    # pulse_6 = [EXPL_F, EXPL_F + 40, EXPL_F + 60]
    # pulse_6 = list(np.array([10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 70, 80, 90, 120, 150, 200, 205, 210, 215, 220, 225], dtype=int))
    # pulse_6 = [EXPL_F, EXPL_F + 1, EXPL_F + 3, EXPL_F + 6, EXPL_F + 8]

    pulse_6.sort()


    if '6' in P.SHS_TO_SHOW:  # EXPL
        _6 = _6_info.Sh_6_info(pulse_6)
        infos[_6.id] = _6

    return infos