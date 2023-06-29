
from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np
import copy

class Sh_1_info(ShInfoAbstract):
    """
    Basically this is the json replacement (also chronicle to some extent).
    Just very basic stuff
    """

    def __init__(_s, pulse, top_point, EXPL_F):
        super().__init__()
        _s.id = '1'
        _s.extent = "static"
        _s.child_names = ['srs', 'lis', 'fs']
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        _s.frames_tot = _s.frame_ss[1] - _s.frame_ss[0]
        _s.init_frames = pulse
        _s.ld = [top_point[0] - 3, top_point[1] - 5]

        _s.zorder = 120  # in fron t of c WHY??? NEW: same as 5

        # pulse_srs = [x + 30 for x in _s.init_frames]  # WHY + 30???
        pulse_srs = [x for x in _s.init_frames]
        _s.srs_gi = {'0': _s.gen_srs_gi(pulse_srs)}  # OBS: sp_gi generated in f class. There is no info class for f.
        _s.srs_gi_init_frames = _s.srs_gi['0']['init_frames']

        # pulse_lis = [100, 190, 200, 210, 220, 250, 300]
        # pulse_lis = list(range(5, P.FRAMES_STOP - 100, 20))
        pulse_lis = random.sample(range(50, P.FRAMES_STOP - 500), int(P.FRAMES_TOT / 40))

        # TODO: Add extra lis for expl and mess with the uniform random
        expl_lis = random.sample(range(EXPL_F, EXPL_F + 1000), 50)
        pulse_lis.extend(expl_lis)
        pulse_lis.sort(reverse=False)
        _s.lis_gi = _s.gen_lis_gi(pulse_lis)

        pulse_fs = [EXPL_F + 40]  # shockwave
        _s.fs_gi = _s.gen_fs_gi(pulse_fs)

        pulse_sps = []  # sp hits down

        _s.sps_gi = {}

    def gen_srs_gi(_s, pulse_srs):
        """
        This has to be provided because the fs are generated w.r.t. sh.
        This is like the constructor input for F class
        """

        srs_gi = {
            'init_frames': copy.deepcopy(pulse_srs),
            'frames_tot': 800,
            'ld': [_s.ld[0] + 5, _s.ld[1]],
            'ld_offset_loc': [0, 1],
            'ld_offset_scale': [15, 10],
            'scale_ss': [0.5, 3],
            # 'frame_ss': _s.frame_ss,
            'v_loc': 50,  # OBS SPECIAL, USES BEFORE
            'v_scale': 7,
            'theta_loc': -0.9,  # -1.6 is straight up
            'theta_scale': 0.2,
            # 'rad_rot': random.uniform(-0.3, -1.9),  # BUG
            'rad_rot_loc': -0.1,
            'rad_rot_scale': 0.05,
            'r_f_d_loc': 0.05,
            'r_f_d_scale': 0.02,
            'up_down': 'up',
            'alpha_y_range': [0, 0.15]
            # 'zorder': 50,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_lis_gi(_s, pulse_lis):

        lis_gi = {
            'init_frames': pulse_lis,
            'frames_tot': None,
            'ld': [_s.ld[0] - 0, _s.ld[1] + 0],
            'ld_offset_loc': [0, 1],
            'ld_offset_scale': [5, 5],
            'zorder': _s.zorder + 10
        }

        return lis_gi

    def gen_fs_gi(_s, pulse):
        """
        This has to be provided because the fs are generated w.r.t. sh.
        This is like the constructor input for F class
        """
        FRAMES_TOT = 120
        fs_gi = {
            'rad_rot': -0.0,
            'init_frames': pulse,
            'frames_tot': FRAMES_TOT,
            'scale_ss': [0.1, 2.0],
            'frame_ss': None,  # simpler with this
            'ld': [_s.ld[0] - 30, _s.ld[1] + 30],
            'x_mov': list(np.linspace(0, -250, num=FRAMES_TOT)),  # SPECIAL
            'y_mov': list(np.linspace(0, 250, num=FRAMES_TOT)),  # SPECIAL
            'alpha_y_range': [0.01, 0.8],
            'zorder': _s.zorder
        }

        return fs_gi





