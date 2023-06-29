import copy

from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np

class Sh_6_info(ShInfoAbstract):
    """
    Basically this is the json replacement (also chronicle to some extent).
    Just very basic stuff
    """

    def __init__(_s, pulse, top_point):
        super().__init__()
        _s.id = '6'

        _s.extent = "static"
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        # _s.frames_tot = _s.frame_ss[1] - _s.frame_ss[0]  # ONLY ONE WHO USES .
        _s.zorder = 95

        _s.ld = top_point
        _s.child_names = ['fs', 'srs']
        _s.fs_gi = _s.gen_fs_gi(pulse)  # OBS: sp_gi generated in f class. There is no info class for f.

        if P.A_SPS == 1:
            _s.sps_gi = _s.gen_sps_gi(pulse)

    def gen_fs_gi(_s, pulse):
        """
        This has to be provided because the fs are generated w.r.t. sh.
        This is like the constructor input for F class
        """
        FRAMES_TOT = 600  # MUST BE HIGHTER THAN SP.FRAMES_TOT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        fs_gi = {
            'rad_rot': -0.2,
            'init_frames': pulse,
            'frames_tot': FRAMES_TOT,
            'scale_ss': [0.01, 1.1],
            'frame_ss': None,  # simpler with this
            'ld': [_s.ld[0] - 2, _s.ld[1]],
            'x_mov': list(np.linspace(0, -15, num=FRAMES_TOT)),  # SPECIAL
            'zorder': 5
        }

        return fs_gi

    def gen_sps_gi(_s, init_frames):
        """
        UPDATE: THESE ARE NO LONGER CHILDREN OF F,
        THEIR INIT FRAMES CAN BE SET BY F THOUGH.
        """
        sps_gi = {
            'init_frames': init_frames,  # ONLY FOR THIS TYPE
            'frames_tot': 300,  # MUST BE LOWER THAN SP.FRAMES_TOT. MAYBE NOT. INVOLVED IN BUG
            # 'v_loc': 50, 'v_scale': 20,
            # 'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
            # 'theta_loc': 1.52, 'theta_scale': 0.2,
            # 'r_f_d_loc': 0.15, 'r_f_d_scale': 0.23,
            'sp_len_loc': 30, 'sp_len_scale': 5,  # this means that everything will be long, and only slow ones survive
            # 'rad_rot': 0.1,
            'ld': _s.ld,  # in
            'ld_offset_loc': [0, 0],  # NOT USED!!!
            'ld_offset_scale': [125, 5],
            'rgb_start': [0.4, 0.7],  #
            'rgb_theta_diff_c': 0.2,
            'rgb_v_diff_c': 0.001,
            'up_down': 'up'
            # NEED ZORDER
        }

        if P.POST:
            sps_gi['alpha_y_range'] = [1, 1]
            sps_gi['rgb_start'] = [0.7, 0.99]
            sps_gi['r_f_d_loc'] = [0.3]
            sps_gi['r_f_d_scale'] = [0.05]
            sps_gi['theta_loc'] = np.pi / 2
            sps_gi['theta_scale'] = 0.1
            sps_gi['v_loc'] = 220
            sps_gi['v_scale'] = 10
            sps_gi['zorder'] = 1000

        return sps_gi
