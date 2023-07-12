"""spark"""

from src.gen_extent_triangles import *
from src.layers.abstract import AbstractLayer, AbstractSSS
import P as P
import numpy as np
from copy import deepcopy
import random
from src.projectile_functions import *
from src.gen_trig_fun import gen_alpha, min_max_normalization
from src.trig_functions import _sigmoid
import matplotlib as mpl

class Sp(AbstractLayer, AbstractSSS):

    def __init__(_s, sh, id_int, f=None):
        AbstractLayer.__init__(_s)

        _s.sh = sh
        _s.id = sh.id + "_f" + "_sp_" + str(id_int)

        # if f != None:
        _s.id = sh.id + "_f" + "_sp_" + str(id_int)
        _s.f = f
        _s.gi = deepcopy(f.sps_gi)
        _s.sp_lens = None

        AbstractSSS.__init__(_s, sh, _s.id)

    def gen_scale_vector(_s):

        scale_ss = []
        return scale_ss

    def dyn_gen(_s, i, gi=None):

        """
        Basically everything moved from init to here.
        This can only be called when init frames are synced between
        """

        # if gi == None:  # gi pre-computed
        #     assert(_s.f != None)
        #     _s.gi = deepcopy(_s.f.sps_gi)
        #
        #     _s.gi['r_f_d_type'] = 'after'  # after is what is kept

        _s.init_frame = _s.set_init_frame(i)

        _s.finish_info()

        '''New: Shift y values down linearly'''

        y_do_shift_start = 50
        y_do_shift_stop = 100
        y_do_shift = random.randint(y_do_shift_start, y_do_shift_stop)

        _s.set_frames_tot(y_do_shift)  # SAME

        _s.xy_t = simple_projectile(v=_s.gi['v'], theta=_s.gi['theta'], rc=1,
                                    frames_tot=_s.gi['frames_tot'], up_down=_s.gi['up_down'], gi=_s.gi)

        _s.xy = shift_projectile(_s.xy_t, origin=(_s.gi['ld'][0] + _s.gi['ld_offset'][0],
                                                  _s.gi['ld'][1] + _s.gi['ld_offset'][1]),
                                 frames_tot_d=_s.gi['frames_tot'],
                                 gi=_s.gi)

        '''Regenerate y based on theta. If theta is close to pi/2, then create linspace for y after top, with 
        fewer frames than frames_tot. Update frames_tot'''

        _s.sp_lens = _s.set_sp_lens(y_do_shift)  # PERHAPS THETA INSTEAD?

        # y_do_shifts_input = np.linspace(0, y_do_shift, len(_s.xy))
        # y_do_shifts_max = 400 ** 1.05
        # y_do_shifts = y_do_shifts_input ** 1.2
        #
        # x_shift_input = np.linspace(0, 100, len(_s.xy))
        # x_shifts = x_shift_input ** 1.3
        #
        # _s.xy[:, 1] += y_do_shifts.T
        #
        # for i in range(len(_s.xy) - 1):
        #     x = _s.xy[i, 0]
        #     x_shift = x_shifts[i]
        #     # if x < _s.gi['ld'][0]:
        #     if x < _s.xy[i + 1, 0]:
        #         _s.xy[i, 0] -= x_shift
        #     else:
        #         _s.xy[i, 0] += x_shift


        brkp = 5
        '''Add check to see whether sp ends near middle, if so make it faster'''

        # _s.xy = shift_projectile(_s.xy_t, origin=(_s.gi['ld'][0] + _s.gi['ld_offset'][0],
        #                                           _s.gi['ld'][1] + _s.gi['ld_offset'][1]),
        #                          frames_tot_d=frames_tot_and_d,
        #                          up_down=_s.gi['up_down'],
        #                          r_f_d_type=before_after)

        # _s.alphas = np.linspace(0.6, 0.0, num=len(_s.xy))

        # if _s.f != None:
        _s.alphas = gen_alpha(_s, frames_tot=len(_s.xy), y_range=_s.gi['alpha_y_range'])

        # _s.alphas = np.sin(list(range(0, int(_s.gi['frames_tot'] / 2 * np.pi))))
        if _s.alphas[0] > 0.3:
            asdf = 5
        assert (len(_s.alphas) == len(_s.xy))
        # assert (_s.gi['frames_tot'] == len(_s.alphas))

        # zorder set from gi in abstract class

    def set_init_frame(_s, i):

        # gi = None
        # init_frame = None
        #
        # if _type == 'sh0':
        #     assert(i in _s.sh.gi.sps_init_frames)  # at this point this is the same gi as _s.sh.gi.sps_gi
        #     gi = deepcopy(_s.sh.gi.sps_gi0)  # could take it directly from sh but this is simpler
        #     assert (i in gi['init_frames'])
        #     index_init_frames = gi['init_frames'].index(i)
        #     init_frame = gi['init_frames'][index_init_frames] + random.randint(0, gi['init_frame_max_dist'])
        # elif _type == 'sh2':
        #     # assert(i in _s.gi['init_frames'])
        #     gi = deepcopy(_s.sh.gi.sps_gi2)
        #     assert (i in gi['init_frames'])
        index_init_frames = _s.gi['init_frames'].index(i)
        init_frame = _s.gi['init_frames'][index_init_frames] + random.randint(0, _s.gi['init_frame_max_dist'])

        # _s.gi['r_f_d_type'] = 'after'  # after means what is kept

        return init_frame

    def finish_info(_s):

        """

        """

        _s.gi['v'] = max(30, abs(np.random.normal(loc=_s.gi['v_loc'], scale=_s.gi['v_scale'])))
        theta = np.random.normal(loc=_s.gi['theta_loc'], scale=_s.gi['theta_scale'])  # + np.pi / 2
        _s.gi['theta'] = theta

        dist_to_straight_up = abs(theta - np.pi / 2)
        # _s.gi['frames_tot'] = int(_s.gi['frames_tot'] - dist_to_straight_up * 10)  # relates to speed
        # _s.gi['v'] = _s.gi['v'] + 50 * dist_to_straight_up  # the further from middle, the more. THIS IS ANSWER TO SPECIAL FAST ONES
        _s.gi['v'] = max(30, _s.gi['v'])

        if dist_to_straight_up < 0.1 and _s.gi['v'] > 45:  # frames tot updated elsewhere
            _s.gi['out_screen'] = True

        # _s.gi['r_f_d'] = max(0.001, np.random.normal(loc=_s.gi['r_f_d_loc'], scale=_s.gi['r_f_d_scale']))
        _s.gi['ld_offset'] = [np.random.normal(loc=_s.gi['ld_offset_loc'][0], scale=_s.gi['ld_offset_scale'][0]),
                              np.random.normal(loc=_s.gi['ld_offset_loc'][1], scale=_s.gi['ld_offset_scale'][1])]

        # '''Colors'''
        # 0
        start = random.uniform(_s.gi['rgb_start'][0], _s.gi['rgb_start'][1])  # starts hot
        theta_diff = abs(theta - _s.gi['theta_loc'])  # less hot if theta is far from mean
        v_diff = _s.gi['v_loc'] - _s.gi['v']  # less hot for faster ones, neg if its too fast
        '''color darkened for fast ones'''
        start = min(_s.gi['rgb_start'][1], start - _s.gi['rgb_theta_diff_c'] * theta_diff + \
                    _s.gi['rgb_v_diff_c'] * v_diff)
        end = max(0.3, random.uniform(0.3, start - 0.1))

        x = np.linspace(start, end, _s.gi['frames_tot'])  # no need to flip since it starts hot
        rgb = mpl.colormaps['afmhot'](x)[:, 0:3]  # starts as cold

        _s.R = rgb[:, 0]
        _s.G = rgb[:, 1]
        _s.B = rgb[:, 2]

    def set_sp_lens(_s, y_do_shift):
        """y_do_shift is currently hardcoded"""

        sp_len_start = 2

        if _s.gi['out_screen'] == True:
            sp_lens = np.linspace(sp_len_start, 6, num=_s.gi['frames_tot'], dtype=int)
            return sp_lens

        f0 = abs(int(np.random.normal(loc=_s.gi['sp_len_stop_loc'], scale=_s.gi['sp_len_stop_scale'])))  # terrain
        f1 = 0.6 * (y_do_shift - 50)  # OOOOOOBBS

        sp_len_stop = 0.0 * f0 + 1.0 * f1
        '''Assumed range: 100 - 200'''
        sp_len_stop = max(3, sp_len_stop)
        sp_len_stop = min(6, sp_len_stop)
        if _s.gi['special']:
            sp_len_stop = 10
        sp_lens = np.linspace(sp_len_start, sp_len_stop, num=_s.gi['frames_tot'], dtype=int)

        return sp_lens

    def set_frames_tot(_s, y_do_shift):

        """Uses y"""
        if _s.gi['out_screen'] == True:
            pass
        else:
            # y_do_shift = _s.xy[:, 1][-1] - _s.gi['ld'][1]
            frames_to_remove = int(0.0 * y_do_shift)
            _s.gi['frames_tot'] -= frames_to_remove







