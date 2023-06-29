
from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np
import copy
from src.trig_functions import min_max_normalization

class Sh_7_info(ShInfoAbstract):
    """
    Extras. For now try to do just 1 at init_frame with low alpha.
    Basically this is the json replacement (also chronicle to some extent).
    Just very basic stuff
    """

    def __init__(_s, pulse, pulse_dots, top_point):  # EXTRAS1: srs tied to ls, sps dots
        super().__init__()
        _s.id = '7'
        _s.extent = "static"
        _s.child_names = ['ls', 'srs', 'sps']
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        _s.init_frames = pulse
        _s.ld = top_point

        _s.ls_gi, pulse_srs0 = _s.gen_ls_gi(pulse)  # NO DYN_GEN
        pulse_srs1 = _s.gen_pulse_srs7(pulse_srs0)  # 0: before extending for each sr
        _s.srs_gi = {'0': _s.gen_srs_gi(pulse_srs1)}
        _s.srs_gi_init_frames = _s.srs_gi['0']['init_frames']

        # init_frames_sp0 = [20]
        # init_frames_sp1 = [40]  # 150 is init_frame_max_dist
        # init_frames_sp2 = [60]  # 150 is init_frame_max_dist
        # init_frames_sp3 = [pulse[3] - 100, pulse[3], pulse[3] + 100]  # 150 is init_frame_max_dist

        # pulse_7_sps_dots0 = [EXPL_F - 50, EXPL_F - 20, EXPL_F, EXPL_F + 80, EXPL_F + 150]  # top of mt
        # pulse_7_sps_dots1 = [EXPL_F + 101, EXPL_F + 151, EXPL_F + 101, EXPL_F + 351]  # other locs
        # pulse_7_sps_dots2 = [EXPL_F + 201, EXPL_F + 251, EXPL_F + 301, EXPL_F + 351]  # other locs

        # pulse_dots = _s.gen_pulse_dots(pulse_dots)
        _s.sps_gi0 = _s.gen_sps_gi0(pulse_dots[0:6])
        _s.sps_gi1 = _s.gen_sps_gi1(pulse_dots[6:12])
        # _s.sps_gi2 = _s.gen_sps_gi2(pulse_dots[12:18])
        _s.sps_gi3 = _s.gen_sps_gi3(pulse_dots[18:24])
        _s.sps_gi4 = _s.gen_sps_gi4(pulse_dots[24:])  # SPECIAL sky
        # _s.sps_gi_init_frames = [y for x in pulse_dots for y in x]  # FLATTENING + init_frames_sp1 + init_frames_sp2
        _s.sps_gi_init_frames = pulse_dots  # FLATTENING + init_frames_sp1 + init_frames_sp2

        _s.sps_gi = {  # NOT LINKED TO LS
            '0': _s.sps_gi0,
            '1': _s.sps_gi1,
            # '2': _s.sps_gi2
            '3': _s.sps_gi3,
            '4': _s.sps_gi4
        }

        _s.zorder = 120

    def gen_ls_gi(_s, pulse):
        """
        SHARED FOR THE SAME SH. Kind of... makes sense. ld is used for extent, but they are modified
        for each l in l class finish info.
        """

        # lif0, lif1 = _s.distribute_pulse_for_ls(pulse)  # l_init_frame
        lif0 = [pulse[0]]
        lif1 = [pulse[1]]
        lif2 = [pulse[2]]
        lif3 = [pulse[3]]

        pulse_for_srs = copy.deepcopy(pulse)

        for i in range(1, 26):
            lif0.append(pulse[0] + 101 * i)
            lif1.append(pulse[1] + 101 * i)
            lif2.append(pulse[2] + 101 * i)
            lif3.append(pulse[3] + 101 * i)

            pulse_for_srs.extend([pulse[0] + 101 * i,
                                  pulse[1] + 101 * i,
                                  pulse[2] + 101 * i,
                                  pulse[3] + 101 * i])

        l_init_frames = lif0 + lif1 + lif2 + lif3
        l_init_frames.sort()
        ls_gi = {
            'init_frames_all': l_init_frames,
            'lif0': lif0,
            'lif1': lif1,
            'lif2': lif2,
            'lif3': lif3,
            'frames_tot0': 100,  # LETS KEEP IT
            'frames_tot1': 100,
            'frames_tot2': 100,
            'frames_tot3': 100,
            'ld': _s.ld,
            'ld0': [_s.ld[0] + 12, _s.ld[1] + 152],
            'ld1': [_s.ld[0] + 82, _s.ld[1] + 148],
            'ld2': [_s.ld[0] - 95, _s.ld[1] + 110],
            'ld3': [_s.ld[0] + 135, _s.ld[1] + 235],  # 108 235
            'frame_ss': _s.frame_ss,
            'zorder': 120  # 3 is 110
        }

        return ls_gi, pulse_for_srs

    def gen_pulse_srs7(_s, pulse):

        pulse_srs = []
        for init_frame in pulse:
            for i in range(-10, 10, 6):  # 3ish total for each ls
                init_frame_sr_cand = init_frame + i
                if init_frame_sr_cand not in pulse_srs:
                    pulse_srs.append(init_frame_sr_cand)

        return pulse_srs

    def gen_srs_gi(_s, pulse_srs):
        """
        Tied to ls!
        """

        srs_gi = {
            'init_frames': copy.deepcopy(pulse_srs),
            'frames_tot': 300,
            'ld': None,  # finish_info
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [10, 6],
            'scale_ss': [0.01, 1.2],  # assumed big pics
            # 'frame_ss': _s.frame_ss,
            'v_loc': 25,  # OBS SPECIAL, USES BEFORE
            'v_scale': 5,
            'theta_loc': -0.3,  # -1.6 is straight up
            'theta_scale': 0.05,
            'rad_rot_loc': -0.2,
            'rad_rot_scale': 0.1,
            'r_f_d_loc': 0.05,
            'r_f_d_scale': 0.01,
            'up_down': 'up',
            'alpha_y_range': [0, 0.2],
            'zorder': 200,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    # def gen_pulse_dots(_s, pulse_dots):
    #     """Distances are same for all pulses
    #     frames_tot: 120 (from below)
    #     """
    #
    #     # pulse_dots = []
    #
    #     '''OBS SAME FRAME CANT BE USED. BUT AS LONG AS NOT, MANY ARE LAUNCHED'''
    #     # offset0 = 160  # test it
    #     # offset1 = 440
    #     # offset2 = 10  # NOT USED
    #     # offset3 = 500
    #     # offset4 = 450  # 450
    #     #
    #     # pulse_dots = [
    #     #     [x + offset0 for x in pulse_dots],  # NEED MORE HERE
    #     #     [x + offset1 for x in pulse_dots],
    #     #     [x + offset2 for x in pulse_dots],
    #     #     [x + offset3 for x in pulse_dots],
    #     #     [x + offset4 for x in pulse_dots]
    #     # ]
    #
    #     return pulse_dots

    def gen_sps_gi0(_s, init_frames_sp):

        """
        UPPER
        MATCHED WITH ls gi, BUT THEYRE NOT CHILDREN AS FOR F -> SP (bcs problem there is that when F dies, then
        so does sp, so f has to last longer than sp).
        top left one
        THESE ARE AVERAGES
        r_f_s gives ratio of frames that should be discarded, i.e. the ratio that the sp should
        climb up the projectile (before shifting)

        OBS init_frame is set as random.randint(0, 100) in dyn_gen() SHOULD BE MOVED HERE.

        """

        sps_gi = {
            'gi_id': '0',
            'init_frames': init_frames_sp,
            'frames_tot': 400,  # NEEDS TO MATCH WITH EXPL
            'init_frame_max_dist': 200,  # OBS THIS MUST BE SHORTER
            'v_loc': 80, 'v_scale': 30,
            # 'num_loc': P.NUM_SPS_L, 'num_scale': P.NUM_SPS_L / 2,
            'theta_loc': -1.6, 'theta_scale': 1,  # neg is left  with straight down= -1.6, little bit to left = -1.3
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.3,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 2, 'sp_len_scale': 24,
            'rgb_start': [0.4, 0.7],  # ONLY START (between these 2)
            'rgb_theta_diff_c': 0.1,  # prob not used due to minimum broken
            'rgb_v_diff_c': 0.01,
            'ld': [_s.ld[0] - 5, _s.ld[1] + 14],
            'ld_offset_loc': [-0, 0],  # NOT USED, CENTERED ON ZERO AND USES ld ABOVE
            'ld_offset_scale': [5, 130],  # SCALE HERE IS USED AS INPUT TO NORMAL
            # 'R_ss': [0.9, 1], 'R_scale': 0.2,
            # 'G_ss': [0.5, 0.2], 'G_scale': 0.15,
            # 'B_ss': [0.2, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'alpha_y_range': [0.01, 0.3],
            'up_down': 'down'
        }

        return sps_gi

    def gen_sps_gi1(_s, init_frames_sp):

        """
        MIDDLE

        THESE ARE AVERAGES
        r_f_s gives ratio of frames that should be discarded, i.e. the ratio that the sp should
        climb up the projectile (before shifting)
        """

        sps_gi = {
            'gi_id': '1',
            'init_frames': init_frames_sp,
            'frames_tot': 1500,  # NEEDS TO MATCH WITH EXPL
            'init_frame_max_dist': 600,  # 100 OBS THIS MUST BE SHORTER
            'v_loc': 60, 'v_scale': 50,
            # 'num_loc': P.NUM_SPS_L, 'num_scale': P.NUM_SPS_L / 2,
            'theta_loc': -1.6, 'theta_scale': 1,  # neg is left  with straight down= -1.6, 0=
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.3,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 2, 'sp_len_scale': 164,
            'rgb_start': [0.3, 0.5],  #
            'rgb_theta_diff_c': 0.0,
            'rgb_v_diff_c': 0.0001,
            'ld': [_s.ld[0] - 5, _s.ld[1] + 90],  #60
            'ld_offset_loc': [-0, 0],  # NOT USED, CENTERED ON ZERO AND USES ld ABOVE
            'ld_offset_scale': [40, 15],  # SCALE HERE IS USED AS INPUT TO NORMAL
            'alpha_y_range': [0.01, 0.4],
            'up_down': 'down'
        }

        # 160, 77, 36  -> 76, 42, 28

        return sps_gi

    # def gen_sps_gi2(_s, init_frames_sp):
    #
    #     """
    #     MIDDLE
    #
    #     THESE ARE AVERAGES
    #     r_f_s gives ratio of frames that should be discarded, i.e. the ratio that the sp should
    #     climb up the projectile (before shifting)
    #     """
    #
    #     sps_gi = {
    #         'gi_id': '2',  # NOT USED
    #         'init_frames': init_frames_sp,
    #         'frames_tot': 600,  # NEEDS TO MATCH WITH EXPL
    #         'init_frame_max_dist': 300,  # OBS THIS MUST BE SHORTER
    #         'v_loc': 40, 'v_scale': 10,
    #         # 'num_loc': P.NUM_SPS_L, 'num_scale': P.NUM_SPS_L / 2,
    #         'theta_loc': -1.6, 'theta_scale': 1,  # neg is left  with straight down= -1.6, 0=
    #         'r_f_d_loc': 0.1, 'r_f_d_scale': 0.3,
    #         'r_f_d_type': 'after',  # which part of r_f_d to use
    #         'sp_len_loc': 2, 'sp_len_scale': 164,
    #         'rgb_start': [0.3, 0.5],  #
    #         'rgb_theta_diff_c': 0.0,
    #         'rgb_v_diff_c': 0.01,
    #         'ld': [_s.ld[0] - 5, _s.ld[1] + 100],
    #         'ld_offset_loc': [-0, 0],  # NOT USED, CENTERED ON ZERO AND USES ld ABOVE
    #         'ld_offset_scale': [40, 15],  # SCALE HERE IS USED AS INPUT TO NORMAL
    #         'alpha_y_range': [0.01, 0.01],
    #         'up_down': 'down'
    #     }
    #
    #     # 160, 77, 36  -> 76, 42, 28
    #
    #     return sps_gi

    def gen_sps_gi3(_s, init_frames_sp):

        """
        lower left one
        THESE ARE AVERAGES
        r_f_s gives ratio of frames that should be discarded, i.e. the ratio that the sp should
        climb up the projectile (before shifting)
        """

        sps_gi = {
            'gi_id': '3',
            'init_frames': init_frames_sp,
            'frames_tot': 2000,  # NEEDS TO MATCH WITH EXPL. Probably exceeds max but whatever
            'init_frame_max_dist': 400,  # OBS THIS MUST BE SHORTER
            'v_loc': 30, 'v_scale': 10,
            # 'num_loc': P.NUM_SPS_L, 'num_scale': P.NUM_SPS_L / 2,
            'theta_loc': -1.6, 'theta_scale': 1,  # neg is left  with straight down= -1.6, 0=
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.3,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 2, 'sp_len_scale': 4,
            'rgb_start': [0.3, 0.5],  #
            'rgb_theta_diff_c': 0.0,
            'rgb_v_diff_c': 0.0001,
            'ld': [_s.ld[0] - 5, _s.ld[1] + 170],
            'ld_offset_loc': [-0, 0],  # NOT USED, CENTERED ON ZERO AND USES ld ABOVE
            'ld_offset_scale': [100, 15],  # SCALE HERE IS USED AS INPUT TO NORMAL
            'alpha_y_range': [0.01, 0.3],
            'up_down': 'down'
        }

        # 160, 77, 36  -> 76, 42, 28

        return sps_gi

    def gen_sps_gi4(_s, init_frames_sp):

        """
        """

        sps_gi = {
            'gi_id': '4',
            'init_frames': init_frames_sp,
            'frames_tot': 400,  # NEEDS TO MATCH WITH EXPL
            'init_frame_max_dist': 150,  # OBS THIS MUST BE SHORTER
            'v_loc': 160, 'v_scale': 20,
            # 'num_loc': P.NUM_SPS_L, 'num_scale': P.NUM_SPS_L / 2,
            'theta_loc': -1.5, 'theta_scale': 0.01,  # neg is left with straight down= -1.6, 0=
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.3,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 2, 'sp_len_scale': 80,
            'rgb_start': [0.3, 0.6],  #
            'rgb_theta_diff_c': 0.1,
            'rgb_v_diff_c': 0.01,
            'ld': [_s.ld[0] - 20, _s.ld[1] - 10],
            'ld_offset_loc': [-0, 0],  # NOT USED, CENTERED ON ZERO AND USES ld ABOVE
            'ld_offset_scale': [90, 15],  # SCALE HERE IS USED AS INPUT TO NORMAL
            'alpha_y_range': [0.01, 0.07],
            'up_down': 'down'
        }

        # 160, 77, 36  -> 76, 42, 28

        return sps_gi

    # def gen_sps_gi3(_s, init_frames_sp):
    #
    #     """
    #     lower left one
    #     THESE ARE AVERAGES
    #     r_f_s gives ratio of frames that should be discarded, i.e. the ratio that the sp should
    #     climb up the projectile (before shifting)
    #     """
    #
    #     sps_gi = {
    #         'gi_id': '3',
    #         'init_frames': init_frames_sp,
    #         'frames_tot': 150,
    #         'init_frame_max_dist': 100,  # random num of frames in future from init frame
    #         'v_loc': 100, 'v_scale': 10,
    #         # 'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
    #         'theta_loc': -1.1, 'theta_scale': 0.1,
    #         'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
    #         'r_f_d_type': 'after',  # which part of r_f_d to use
    #         'rgb_start': [0.4, 0.45],  #
    #         'rgb_theta_diff_c': 1,
    #         'rgb_v_diff_c': 0.01,
    #         'sp_len_loc': 5, 'sp_len_scale': 15,
    #         'ld': [_s.ld[0] - 0, _s.ld[1] + 15],
    #         'ld_offset_loc': [0, 2],
    #         'ld_offset_scale': [1, 1],
    #         'R_ss': [0.8, 1], 'R_scale': 0.2,
    #         'G_ss': [0.4, 0.2], 'G_scale': 0.2,
    #         'B_ss': [0.1, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
    #         'alpha_y_range': [0.01, 0.9],
    #         'up_down': 'down'
    #     }
    #
    #     # 160, 77, 36  -> 76, 42, 28
    #
    #     return sps_gi





