import copy

# from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np
from scipy import stats

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
        NUM_RANDS = 40

        fs_gi = {
            'rad_rot': -0.2,
            'init_frames': pulse,
            'frames_tot': FRAMES_TOT,  # only used for init
            'scale_ss': [0.01, 1.1],
            'frame_ss': None,  # simpler with this
            'ld': [None, None],  # set at init
            'left_mid': 640,
            'left_offsets': None,  # BELOW [-500, 500] num doesnt matter cuz pos = random.randint(0, 20)
            # 'downs_sps': [],
            'theta_loc': None,  # set at init from offsets
            'theta_offsets': None,  # list(np.linspace(0.3, -0.3, num=NUM_RANDS)), #[0.5, -0.5],
            'init_frame_x_offsets': list(np.linspace(40, 0, num=NUM_RANDS - 25, dtype=int)) + list(np.linspace(0, 60, num=NUM_RANDS - 15, dtype=int)),
            'init_frames_dirichlet': None,
            # 'x_mov': list(np.linspace(0, -15, num=FRAMES_TOT)),  # SPECIAL
            'zorder': 5
        }

        '''LEFT OFFSETS'''
        _normal = stats.norm(loc=640, scale=200)
        bounds_for_range = _normal.cdf([0, 1280])
        pp = np.linspace(*bounds_for_range, num=NUM_RANDS)
        left_offsets = _normal.ppf(pp).astype(int)
        left_offsets[0] = left_offsets[1]
        left_offsets[-1] = left_offsets[-2]
        fs_gi['left_offsets'] = left_offsets

        '''THETA OFFSETS. OBS ONLY POSITIVE'''
        # distribution = stats.norm(loc=np.pi, scale=4 * np.pi)
        _normal = stats.norm(loc=np.pi/2, scale=np.pi/4)
        # _normal = stats.norm(loc=np.pi/2, scale=np.pi/2)
        # distribution_pdf = _normal.pdf(np.linspace(0, np.pi, num=NUM_RANDS))
        distribution_pdf = _normal.pdf(np.linspace(0.25 * np.pi, 0.75 * np.pi, num=NUM_RANDS))
        # theta_offsets = distribution_pdf.ppf(np.linspace(0, 4, num=NUM_RANDS)
        thetas = _normal.ppf(distribution_pdf)
        thetas[0] = thetas[1]
        thetas[-1] = thetas[-2]
        # theta_offsets = _normal.ppf(distribution_pdf)
        # theta_offsets += np.pi /
        fs_gi['thetas'] = thetas


        assert(len(fs_gi['init_frame_x_offsets']) == NUM_RANDS)

        dirichlet_delays = list(np.random.random_integers(100, 200, size=NUM_RANDS))
        init_frames_dirichlet = np.random.dirichlet(dirichlet_delays, size=len(fs_gi['init_frames'])) * 1000
        fs_gi['init_frames_dirichlet'] = init_frames_dirichlet.astype(int)
        aa = fs_gi['init_frames_dirichlet'].shape[1]
        for col in range(fs_gi['init_frames_dirichlet'].shape[1]):
            if random.random() < 0.5:
                assert(max(fs_gi['init_frames_dirichlet'][:, col]) < 100)  # otherwise it can start before anim begins
                fs_gi['init_frames_dirichlet'][1:, col] *= -1

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
            'frames_tot': 400,  # MUST BE LOWER THAN SP.FRAMES_TOT. MAYBE NOT. INVOLVED IN BUG
            'v_loc': 50, 'v_scale': 4,  # 50 THIS IS HOW HIGH THEY GO (not how far down)
            'theta_scale': 0.01,  # 0.1 unit circle straight up
            'sp_len_start_loc': 1, 'sp_len_start_scale': 1,
            'sp_len_stop_loc': 4, 'sp_len_stop_scale': 1,  # this only cov  ers uneven terrain
            # 'init_frame_max_dist': 10,
            'special': False,
            'ld_init': [None, None],  # set by f
            'ld': [None, None],  # set by f
            'ld_offset_loc': [0, 0],  # NEW: Assigned when inited
            'ld_offset_scale': [50, 3],  # [125, 5]
            'rgb_start': [0.4, 0.7],  #
            'rgb_theta_diff_c': 0.2,
            'rgb_v_diff_c': 0.001,
            'up_down': 'up',
            'out_screen': False,
            'zorder': 1000
        }

        return sps_gi
