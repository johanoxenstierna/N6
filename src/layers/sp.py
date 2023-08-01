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
        _s.ars_bool = 0

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

        _s.finish_info()

        '''New: Shift y values down linearly'''

        _s.set_frames_tot()  # SAME

        _s.xy_t = simple_projectile(gi=_s.gi)

        if _s.gi['ld'][0] < _s.f.gi['left_mid']:  # flip x values
            _s.xy_t[:, 0] = -_s.xy_t[:, 0]

        _s.xy = shift_projectile(_s.xy_t, origin=(_s.gi['ld'][0] + _s.gi['ld_offset'][0],
                                                  _s.gi['ld'][1] + _s.gi['ld_offset'][1]), gi=_s.gi)

        '''out_screen if xy outside'''
        neg = np.argwhere(_s.xy[:, 1] < 0)
        if len(neg) > 20:
            _s.xy[neg[0, 0]:, 1] = -100  # [0, 0] cuz it comes as a single col

        _s.sp_lens = _s.set_sp_lens()  # PERHAPS THETA INSTEAD?

        _s.init_frame = _s.set_init_frame(i)


        _s.alphas = gen_alpha(_s, frames_tot=len(_s.xy), y_range=_s.gi['alpha_y_range'])

        assert (len(_s.alphas) == len(_s.xy))

    def set_init_frame(_s, i):

        index_init_frames = _s.gi['init_frames'].index(i)
        init_frame = _s.gi['init_frames'][index_init_frames] + random.randint(0, _s.gi['init_frame_max_dist'])

        '''OBS special lateness to side ones'''
        if P.NUM_FS == 2:
            pass
        else:
            pass
            # if _s.gi['dist_to_theta_loc'] > 0.15:
            #     init_frame += 40

        return init_frame

    def finish_info(_s):

        """
        """

        _s.gi['ld'] = _s.f.gi['ld']
        _s.gi['theta_loc'] = _s.f.gi['theta_loc']

        _s.gi['y_do_shift_start'] = 50
        _s.gi['y_do_shift_stop'] = 100
        _s.gi['y_do_shift'] = random.randint(_s.gi['y_do_shift_start'], _s.gi['y_do_shift_stop'])

        _s.gi['v'] = abs(np.random.normal(loc=_s.gi['v_loc'], scale=_s.gi['v_scale']))

        _s.gi['theta'] = np.random.normal(loc=_s.gi['theta_loc'], scale=_s.gi['theta_scale'])  # + np.pi / 2

        # _s.gi['theta'] = max(_s.gi['theta_loc'] - 0.23, _s.gi['theta'])  # theta must be larger than
        # _s.gi['theta'] = min(_s.gi['theta_loc'] + 0.23, _s.gi['theta'])  # theta must be lower than

        # TODO: theta also needs to depend on left

        _s.gi['dist_to_theta_loc'] = abs(_s.gi['theta'] - _s.gi['theta_loc'])
        _s.gi['dist_to_theta_0'] = abs(_s.gi['theta'] - np.pi / 2)

        # if _s.gi['dist_to_theta_0'] < 0.2 and _s.gi['v'] > _s.gi['v_loc'] + 0.1 * _s.gi['v_loc']:  # frames tot updated elsewhere
        #     _s.gi['out_screen'] = True

        _s.gi['ld_offset'] = [np.random.normal(loc=_s.gi['ld_offset_loc'][0], scale=_s.gi['ld_offset_scale'][0]),
                              np.random.normal(loc=_s.gi['ld_offset_loc'][1], scale=_s.gi['ld_offset_scale'][1])]

        if _s.gi['theta'] > _s.gi['theta_loc']:
            _s.gi['ld_offset'][0] -= 5  # pointing left=also to the left
        else:
            _s.gi['ld_offset'][0] += 5


        # '''Colors'''
        # 0
        start = random.uniform(_s.gi['rgb_start'][0], _s.gi['rgb_start'][1])  # starts hot
        v_diff = _s.gi['v_loc'] - _s.gi['v']  # less hot for faster ones, neg if its too fast

        '''color darkened for fast ones'''
        start = min(_s.gi['rgb_start'][1], start - _s.gi['rgb_theta_diff_c'] * _s.gi['dist_to_theta_loc'] + \
                    _s.gi['rgb_v_diff_c'] * v_diff)
        end = max(0.3, random.uniform(0.3, start - 0.1))

        x = np.linspace(start, end, _s.gi['frames_tot'])  # no need to flip since it starts hot
        rgb = mpl.colormaps['afmhot'](x)[:, 0:3]  # starts as cold

        _s.R = rgb[:, 0]
        _s.G = rgb[:, 1]
        _s.B = rgb[:, 2]

    def set_sp_lens(_s):
        """y_do_shift is currently hardcoded"""

        sp_len_start = 2

        if _s.gi['out_screen'] == True:
            sp_lens = np.linspace(sp_len_start, 6, num=_s.gi['frames_tot'], dtype=int)
            return sp_lens

        f0 = abs(int(np.random.normal(loc=_s.gi['sp_len_stop_loc'], scale=_s.gi['sp_len_stop_scale'])))  # terrain
        f1 = 0.5 * (_s.gi['y_do_shift'] - _s.gi['y_do_shift_start'])

        sp_len_stop = 0.0 * f0 + 1.0 * f1  # THE MORE DOWN SHIFT, THE LARGER
        '''Assumed range: 100 - 200'''
        sp_len_stop = max(2, sp_len_stop)
        sp_len_stop = min(6, sp_len_stop)
        if _s.gi['special']:  # NOT USED
            sp_len_stop = 80

        # if _s.gi['dist_to_theta_0'] > 0.1 and _s.gi['v'] > _s.gi['v_loc']:  # fast ones to side
        #     sp_len_stop = 3  # this is TRICKY

        sp_lens = np.linspace(sp_len_start, sp_len_stop, num=_s.gi['frames_tot'], dtype=int)

        return sp_lens

    def set_frames_tot(_s):

        """Uses y"""
        if _s.gi['out_screen'] == True:
            pass  # shouldnt be done here
        else:
            # y_do_shift = _s.xy[:, 1][-1] - _s.gi['ld'][1]
            frames_to_remove = int(0.0 * _s.gi['y_do_shift'])
            _s.gi['frames_tot'] -= frames_to_remove







