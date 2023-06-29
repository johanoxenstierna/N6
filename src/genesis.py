
import random

import numpy as np

import P

# from sh_info import shInfoAbstract, _0_info
from sh_info import _0_info, _1_info, _2_info, _3_info, _4_info, _5_info, _6_info, _7_info, _8_info, _9_info

def init_infos():
    '''Creates instance of each info and stores in dict'''
    infos = {}

    # top_point0 = [210, 80]
    # top_point1 = [210, 90]  # aft expl
    # top_point2 = [210, 90]  # for 3 rocks

    top_point0 = [550, 330]
    top_point1 = [550, 350]  # aft expl????
    top_point_c = [550, 340]  # for 3 rocks
    if P.POST:
        top_point_c = [650, 440]
    top_point2 = [550, 330]
    top_point5 = [553, 336]
    top_point6 = [550, 540]
    top_point7 = [560, 330]
    top_point9 = [550, 330]  # change inside
    EXPL_F = 10  # 1300

    # pulse_sr1 = random.sample(range(5, P.FRAMES_STOP - 800), P.NUM_SRS_1)  # 1 (sr)
    # pulse_sr1.sort(reverse=False)
    # pulse_sr1 = [110, 150]  # 1 (sr)

    # pulse_0_fs = random.sample(range(50, EXPL_F + 20), 25 * 3)  # 0 after initial srs
    # pulse_0_fs = random.sample(range(50, EXPL_F - 20), 18)  # 0 after initial srs
    # pulse_0_srs = random.sample(range(20, P.FRAMES_STOP - 600), P.NUM_SRS_0)  # OBS ONLY CLOSE TO 0 fs

    # pulse_3 = [10, 30, 100]  # expl
    pulse_3 = random.sample(range(EXPL_F - 50, EXPL_F + 50), 10)  # post expl FIRST FRAME USED AS REFERENCE FOR C

    # pulse_4 = [110, 180, 200, 231, 300, 350]  # THIS IS FOR LS, 1 PER L SEQUENTIAL
    # pulse_4 = random.sample(range(110, EXPL_F + 50), 10 * 3)
    # pulse_4 = [210, 280, 300, 331]  # THIS IS FOR LS, 1 PER L SEQUENTIAL
    pulse_5 = random.sample(range(EXPL_F - 20, P.FRAMES_STOP - 800), 30 * 3)  # ONLY FS this is num fs post expl ONLY fs
    pulse_5.append(EXPL_F - 20)  # needs to include exact one
    pulse_5.sort(reverse=False)
    # pulse_5 = [10, 250]  # expl

    # pulse_6 = [5, 10, 50, 100]
    # pulse_6 = [EXPL_F, EXPL_F + 5, EXPL_F + 20, EXPL_F + 150, EXPL_F + 180]   # WWWTTTFFF???
    # pulse_6 = [EXPL_F, EXPL_F + 5, EXPL_F + 25, EXPL_F + 50, EXPL_F + 75, EXPL_F + 200, EXPL_F + 225, EXPL_F + 250]  # TOT SP: 600
    pulse_6 = [EXPL_F, EXPL_F + 1, EXPL_F + 3, EXPL_F + 6, EXPL_F + 8]

    # pulse_7 = [10, 40, 80]
    # pulse_7 = [150, 180, 200, 280, 350]

    # pulse_7 = list(range(P.FRAMES_START + 50, P.FRAMES_STOP - 300, 30 * 3))  # THIS DOESNT MAKE SENSE. NEED TO JUST GIVE FIRST FRMAES FOR LS
    pulse_7 = [50, 150, 1200, 180]  # THESE ARE FOR THE 4 LS. REPEATED LATER.
    pulse_dots = [EXPL_F + 350, EXPL_F + 400, EXPL_F + 450, EXPL_F + 500, EXPL_F + 600, EXPL_F + 700,
                  EXPL_F + 401, EXPL_F + 426, EXPL_F + 451, EXPL_F + 476, EXPL_F + 501, EXPL_F + 551,
                  EXPL_F + 0, EXPL_F + 0, EXPL_F + 0, EXPL_F + 0, EXPL_F + 0, EXPL_F + 0,
                  EXPL_F + 503, EXPL_F + 553, EXPL_F + 603, EXPL_F + 653, EXPL_F + 703, EXPL_F + 753,
                  EXPL_F + 604, EXPL_F + 704, EXPL_F + 754, EXPL_F + 804, EXPL_F + 904, EXPL_F + 1004,
                  EXPL_F + 1200, EXPL_F + 1300, EXPL_F + 1400]
    # pulse_dots = [160, 440, 10, 500, 450]

    pulse_8 = None  # this one is specially set inside 8_info

    # pulse_9_tot_inits = (P.FRAMES_STOP - 500) - (EXPL_F + 200)
    # pulse_9 = random.sample(range(EXPL_F + 200, P.FRAMES_STOP - 1000), pulse_9_tot_inits // 2)
    # pulse_9 = random.sample(range(10, 1000), 500)

    # pulse_0_fs.sort()
    # pulse_0_srs.sort()
    # pulse_sr1.sort()
    pulse_3.sort()
    pulse_5.sort()
    pulse_6.sort()
    # pulse_7.sort()  # NOOOO

    if '0' in P.SHS_TO_SHOW:  # BEF EXPL
        _0 = _0_info.Sh_0_info(pulse_0_fs, pulse_0_srs, top_point0)
        infos[_0.id] = _0

    if '1' in P.SHS_TO_SHOW:  # +shockwave ALL OF THEM. LD NEEDS TO WORK FOR BOTH
        _1 = _1_info.Sh_1_info(pulse_sr1, top_point1, EXPL_F)  # OBS shifts pulse_sr1 +30
        infos[_1.id] = _1

    if '2' in P.SHS_TO_SHOW:  # DOWN LEFT
        _2 = _2_info.Sh_2_info(5, EXPL_F, top_point2)  # start_f, expl_f
        infos[_2.id] = _2

    if '3' in P.SHS_TO_SHOW and P.A_CS:  # ROCKS
        _3 = _3_info.Sh_3_info(pulse_3, top_point_c)
        infos[_3.id] = _3

    if '4' in P.SHS_TO_SHOW:  #
        _4 = _4_info.Sh_4_info(1100, EXPL_F, top_point0)
        infos[_4.id] = _4  # DOWN RIGHT

    # 5: 0 but after expl
    if '5' in P.SHS_TO_SHOW:  # POST EXPL
        _5 = _5_info.Sh_5_info(pulse_5, top_point5)
        infos[_5.id] = _5

    if '6' in P.SHS_TO_SHOW:  # EXPL
        _6 = _6_info.Sh_6_info(pulse_6, top_point6)
        infos[_6.id] = _6

    if '7' in P.SHS_TO_SHOW:  # EXTRAS1: srs tied to ls, sps dots. INCLUDES long ones
        _7 = _7_info.Sh_7_info(pulse_7, pulse_dots, top_point7)
        infos[_7.id] = _7

    if '8' in P.SHS_TO_SHOW:  # EXTRAS2: srs upper
        _8 = _8_info.Sh_8_info(top_point0)
        infos[_8.id] = _8
    if '9' in P.SHS_TO_SHOW:  # EXTRAS2: srs upper
        _9 = _9_info.Sh_9_info(pulse_9, top_point9)
        infos[_9.id] = _9

    return infos