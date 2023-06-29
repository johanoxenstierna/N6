import copy

from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np
from scipy.stats import norm

from src.trig_functions import *

class Sh_9_info(ShInfoAbstract):
    """
    Basically this is the json replacement (also chronicle to some extent).
    Just very basic stuff
    """

    def __init__(_s, pulse, top_point):
        super().__init__()

        _s.id = '9'

        _s.extent = "static"
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        _s.frames_tot = _s.frame_ss[1] - _s.frame_ss[0]  # ONLY ONE WHO USES .

        _s.ld = top_point
        _s.child_names = ['srs']
        pulses = _s.distribute_pulse(pulse)

        _s.zorder = 120
        if P.A_SRS == 1:
            _s.srs_gi0 = _s.gen_srs_gi0(pulses[0])  # OBS: sp_gi generated in f class. There is no info class for f.
            _s.srs_gi1 = _s.gen_srs_gi1(pulses[1])  # OBS: sp_gi generated in f class. There is no info class for f.
            _s.srs_gi_init_frames = pulse
            _s.srs_gi = {  # these numbers are because of c!
                '0': _s.srs_gi0,
                '1': _s.srs_gi1,
            }

    def distribute_pulse(_s, pulse):
        """They dont have to be equal in length!"""

        pulses = [[], []]

        pulse.sort()

        X = np.linspace(norm.ppf(0.01), norm.ppf(0.99), len(pulse))
        p0 = norm.pdf(X, loc=-1, scale=2)
        p1 = norm.pdf(X, loc=1, scale=1)

        for i in range(len(pulse)):
            _p0 = p0[i] / (p0[i] + p1[i])
            _p1 = p1[i] / (p0[i] + p1[i])
            i_sel = np.random.choice([0, 1], p=[_p0, _p1])
            pulses[i_sel].append(pulse[i])

        return pulses

    def gen_srs_gi0(_s, pulse):
        """
        This has to be provided because the fs are generated w.r.t. sh.
        This is like the constructor input for F class
        """

        srs_gi = {
            '9_id': '0',
            'init_frames': copy.deepcopy(pulse),
            'frames_tot': 900,
            'ld': [_s.ld[0] - 0, _s.ld[1] - 80],
            'ld_offset_loc': [7, 15],
            'ld_offset_scale': [10, 10],
            'scale_ss': [0.2, 2.5],
            'frame_ss': _s.frame_ss,
            # 'v_loc': 45,
            # 'v_scale': 12,
            'height': 120,  # 92: 150
            'c': 0.017,
            'rad_rot_loc': -0.1,
            'rad_rot_scale': 0.1,
            'alpha_y_range': [0, 0.2],
            'up_down': 'up',  # only used bcs required in shift_projectile
            'zorder_loc': _s.zorder - 2,  # Set in finish_info
            'zorder_scale': 5
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi1(_s, pulse):
        """
        This has to be provided because the fs are generated w.r.t. sh.
        This is like the constructor input for F class
        """

        srs_gi = {
            '9_id': '1',
            'init_frames': copy.deepcopy(pulse),
            'frames_tot': 900,
            'ld': [_s.ld[0] - 13, _s.ld[1] - 5],  # 92: -10, -30
            'ld_offset_loc': [15, 15],
            'ld_offset_scale': [10, 10],
            'scale_ss': [0.1, 2],
            'frame_ss': _s.frame_ss,
            # 'v_loc': 45,
            # 'v_scale': 12,
            'height': 100,
            'c': 1.5,
            'rad_rot_loc': -1,
            'rad_rot_scale': 0.1,
            'alpha_y_range': [0, 0.2],
            'up_down': 'up',  # only used bcs required in shift_projectile
            'zorder_loc': _s.zorder + 30,  # Set in finish_info
            'zorder_scale': 5
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi
