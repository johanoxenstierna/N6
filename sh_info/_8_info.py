
from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np
import copy

class Sh_8_info(ShInfoAbstract):
    """
    Extras. For now try to do just 1 at init_frame with low alpha.
    Basically this is the json replacement (also chronicle to some extent).
    Just very basic stuff
    """

    def __init__(_s, top_point):
        super().__init__()
        _s.id = '8'
        _s.extent = "static"
        _s.child_names = ['srs']
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        _s.ld = top_point

        # pulse_srs = _s.gen_pulse_srs8(pulse)  # NAW: easier to set it for each
        _s.srs_gi = {  # THESE NEED SEPARATION MAINLY BCS OF INIT FRAMES
            '0': _s.gen_srs_gi0(frames_tot=300),
            '1': _s.gen_srs_gi1(frames_tot=300),
            '2': _s.gen_srs_gi2(frames_tot=300),
            '3': _s.gen_srs_gi3(frames_tot=300),
            '4': _s.gen_srs_gi4(frames_tot=700),
            '5': _s.gen_srs_gi5(frames_tot=900),
            '6': _s.gen_srs_gi6(frames_tot=300),
            '7': _s.gen_srs_gi7(frames_tot=300),
            '8': _s.gen_srs_gi8(frames_tot=300),
            '9': _s.gen_srs_gi9(frames_tot=700),
            '10': _s.gen_srs_gi10(frames_tot=700)
        }

        _s.extend_srs_init_frames(EXTEND_PARAM=9)  # TODO
        # _s.srs_gi_init_frames = _s.srs_gi['4']['init_frames']
        out = []
        for key in _s.srs_gi.keys():
            out.extend(_s.srs_gi[key]['init_frames'])
        out.sort(reverse=False)
        temp_debug = out[-1]
        _s.srs_gi_init_frames = out

        # _s.srs_gi_init_frames = [val['init_frames'] for key, val in _s.srs_gi.items()]
        # _s.srs_gi_init_frames = np.asarray(_s.srs_gi_init_frames).flatten()
        # _s.srs_gi_init_frames.sort(reverse=False)

        _s.zorder = None  # set from gi

    def extend_srs_init_frames(_s, EXTEND_PARAM):


        for key, val in _s.srs_gi.items():
            init_frames_out = val['init_frames']
            for i in range(2, EXTEND_PARAM):
                frames_tot = val['frames_tot']
                init_frames1 = [x + (i * (frames_tot + 10)) for x in val['init_frames']]

                if init_frames1[-1] + frames_tot < P.FRAMES_STOP * 0.95:
                    init_frames_out.extend(init_frames1)
                else:
                    print("8 clouds init_frames1[-1] + frames_tot > P.FRAMES_STOP * 0.9")
                adf = 6


            val['init_frames'] = init_frames_out

    def gen_srs_gi0(_s, frames_tot):

        srs_gi = {
            'id': 0,
            'init_frames': [10, 20, 30, 40, 50],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.3, 0],
            'v_linear_scale': [0.1, 0.02],
            'ld': [_s.ld[0] - 200, _s.ld[1] + 50],  # finish_info
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [100, 50],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.1, -0.3),
            'alpha_y_range': [0.1, 0.4],
            'up_down': None,  # key checked for alpha
            'zorder': 80,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi1(_s, frames_tot):
        srs_gi = {
            'id': 1,
            'init_frames': [11, 21, 31, 41, 51],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.1, 0],
            'v_linear_scale': [0.02, 0.02],
            'ld': [_s.ld[0] - 200, _s.ld[1] + 80],  # finish_info
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [100, 10],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.1, -0.3),
            'alpha_y_range': [0.1, 0.3],
            'up_down': None,  # key checked for alpha
            'zorder': 80,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi2(_s, frames_tot):
        srs_gi = {
            'id': 2,
            'init_frames': [12, 22, 32, 42, 52],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.3, 0],
            'v_linear_scale': [0.1, 0.02],
            'ld': [_s.ld[0] - 100, _s.ld[1] - 35],  # finish_info
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [50, 20],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.1, -0.3),
            'alpha_y_range': [0.1, 0.5],
            'up_down': None,  # key checked for alpha
            'zorder': 80,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi3(_s, frames_tot):
        srs_gi = {
            'id': 3,
            'init_frames': [13, 23, 33, 43, 53],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.3, 0],
            'v_linear_scale': [0.15, 0.02],
            'ld': [_s.ld[0] - 120, _s.ld[1] - 30],  # finish_info
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [100, 50],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.1, -0.3),
            'alpha_y_range': [0.1, 0.4],
            'up_down': None,  # key checked for alpha
            'zorder': 80,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi4(_s, frames_tot):

        srs_gi = {
            'id': 4,
            # 'init_frames': [14, 24, 34, 44, 54, 164, 174, 184, 194, 204],  # NO. REPEATS NOT POSSIBLE BCS DYN GEN NOT USED
            'init_frames': [14, 24, 34, 44, 54, 64],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.3, 0],
            'v_linear_scale': [0.02, 0.01],
            'ld': [_s.ld[0] - 100, _s.ld[1] + 50],  # finish_info
            'ld_offset_loc': [0, 0],  # NOT USED
            'ld_offset_scale': [5, 0.1],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.01, -0.02),
            'alpha_y_range': [0.01, 0.2],
            'up_down': None,  # key checked for alpha
            'zorder': 2000,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi5(_s, frames_tot):

        srs_gi = {
            'id': 5,
            'init_frames': [25, 35, 45, 55, 65, 75],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.3, 0],
            'v_linear_scale': [0.02, 0.01],
            'ld': [_s.ld[0] + 250, _s.ld[1] + 60],  # finish_info
            'ld_offset_loc': [0, 0],  # NOT USED
            'ld_offset_scale': [5, 2],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.1, -0.2),
            'alpha_y_range': [0.001, 0.2],
            'up_down': None,  # key checked for alpha
            'zorder': 2000,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi6(_s, frames_tot):
        srs_gi = {
            'id': 6,
            'init_frames': [16, 26, 36, 46, 56],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.3, 0],
            'v_linear_scale': [0.02, 0.01],
            'ld': [_s.ld[0] + 260, _s.ld[1] + 80],  # finish_info
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [100, 10],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.1, -0.2),
            'alpha_y_range': [0.1, 0.3],
            'up_down': None,  # key checked for alpha
            'zorder': 80,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi7(_s, frames_tot):
        srs_gi = {
            'id': 7,
            'init_frames': [17, 27, 37, 47, 57],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.3, 0],
            'v_linear_scale': [0.05, 0.02],
            'ld': [_s.ld[0] + 200, _s.ld[1] + 50],  # finish_info
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [100, 10],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.1, -0.3),
            'alpha_y_range': [0.1, 0.2],
            'up_down': None,  # key checked for alpha
            'zorder': 80,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi8(_s, frames_tot):
        srs_gi = {
            'id': 8,
            'init_frames': [18, 28, 38, 48, 58],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.3, 0],
            'v_linear_scale': [0.15, 0.02],
            'ld': [_s.ld[0] - 60, _s.ld[1] - 5],  # finish_info
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [100, 50],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.1, -0.3),
            'alpha_y_range': [0.1, 0.3],
            'up_down': None,  # key checked for alpha
            'zorder': 80,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi9(_s, frames_tot):
        srs_gi = {
            'id': 9,
            'init_frames': [19, 29, 39, 49, 59],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.3, 0],
            'v_linear_scale': [0.15, 0.02],
            'ld': [_s.ld[0] + 40, _s.ld[1] + 100],  # finish_info
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [5, 2],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.1, -0.3),
            'alpha_y_range': [0.01, 0.2],
            'up_down': None,  # key checked for alpha
            'zorder': 2000,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_srs_gi10(_s, frames_tot):

        srs_gi = {
            'id': 10,
            'init_frames': [60, 70, 80, 90, 100],
            'frames_tot': frames_tot,
            'v_linear_loc': [-0.3, 0],
            'v_linear_scale': [0.03, 0.02],
            'ld': [_s.ld[0] - 150, _s.ld[1] - 30],  # finish_info
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [60, 60],
            'scale_ss': [1, 1],  # assumed big pics
            'rad_rot': random.uniform(-0.1, -0.3),
            'alpha_y_range': [0.1, 0.3],
            'up_down': None,  # key checked for alpha
            'zorder': 80,
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi






