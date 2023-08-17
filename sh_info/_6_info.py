import copy

# from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np

class Sh_6_info:
    """
    Basically this is the json replacement (also chronicle to some extent).
    Just very basic stuff
    """

    def __init__(_s, pulse):
        super().__init__()
        _s.id = '6'

        _s.extent = "static"
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        # _s.frames_tot = _s.frame_ss[1] - _s.frame_ss[0]  # ONLY ONE WHO USES .
        _s.zorder = 95

        _s.child_names = ['fs', 'srs']
        _s.fs_gi = _s.gen_fs_gi(pulse)  # OBS: sp_gi generated in f class. There is no info class for f.
        _s.sps_gi = _s.gen_sps_gi()

    def gen_fs_gi(_s, pulse):
        """
        This has to be provided because the fs are generated w.r.t. sh.
        This is like the constructor input for F class
        """
        FRAMES_TOT = 600  # MUST BE HIGHTER THAN SP.FRAMES_TOT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        NUM_RANDS = 20

        fs_gi = {
            'rad_rot': -0.2,
            'init_frames': pulse,
            'frames_tot': FRAMES_TOT,  # only used for init
            'scale_ss': [0.01, 1.1],
            'frame_ss': None,  # simpler with this
            'ld': [None, None],  # set at init
            'left_mid': 640,
            'left_offsets': list(np.linspace(-500, 500, num=NUM_RANDS)),  # [-500, 500] num doesnt matter cuz pos = random.randint(0, 20)
            # 'downs_sps': [],
            'theta_loc': None,  # set at init from offsets
            'theta_offsets': list(np.linspace(0.5, -0.5, num=NUM_RANDS)), #[0.5, -0.5],
            'init_frame_x_offsets': list(np.linspace(40, 0, num=NUM_RANDS - 15, dtype=int)) + list(np.linspace(0, 60, num=NUM_RANDS - 5, dtype=int)),
            'init_frames_dirichlet': None,
            # 'x_mov': list(np.linspace(0, -15, num=FRAMES_TOT)),  # SPECIAL
            'zorder': 5
        }

        assert(len(fs_gi['init_frame_x_offsets']) == NUM_RANDS)

        dirichlet_delays = list(np.random.random_integers(100, 200, size=NUM_RANDS))
        init_frames_dirichlet = np.random.dirichlet(dirichlet_delays, size=len(fs_gi['init_frames'])) * 100
        fs_gi['init_frames_dirichlet'] = init_frames_dirichlet.astype(int)

        if P.NUM_FS == 2:
            fs_gi['left_offsets'] = [-10, 10]
            fs_gi['theta_offsets'] = [-0.2, 0.2]

        '''When the fs fire'''
        # aa = np.random.dirichlet()

        return fs_gi

    def gen_sps_gi(_s):
        """
        UPDATE: THESE ARE NO LONGER CHILDREN OF F,
        THEIR INIT FRAMES CAN BE SET BY F THOUGH.
        """
        sps_gi = {
            'alpha_y_range': [0.5, 1.0],
            'init_frames': None,  # ONLY FOR THIS TYPE
            'frames_tot': 200,  # MUST BE LOWER THAN SP.FRAMES_TOT. MAYBE NOT. INVOLVED IN BUG
            'v_loc': 50, 'v_scale': 4,  # 50 THIS IS HOW HIGH THEY GO (not how far down)
            'theta_scale': 0.2,  # 0.1 unit circle straight up
            'sp_len_start_loc': 1, 'sp_len_start_scale': 1,
            'sp_len_stop_loc': 4, 'sp_len_stop_scale': 1,  # this only covers uneven terrain
            # 'init_frame_max_dist': 10,
            'special': False,
            'ld': [None, None],  # set by f
            'ld_offset_loc': [0, 0],  # NEW: Assigned when inited
            'ld_offset_scale': [40, 3],  # [125, 5]
            'rgb_start': [0.4, 0.7],  #
            'rgb_theta_diff_c': 0.2,
            'rgb_v_diff_c': 0.001,
            'up_down': 'up',
            'out_screen': False,
            'zorder': 1000
        }

        return sps_gi
