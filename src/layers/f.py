

import numpy as np
from copy import deepcopy

import P as P
from src.gen_extent_triangles import *
from src.layers.abstract import AbstractLayer, AbstractSSS
from src.gen_trig_fun import gen_alpha  #, gen_scale_lds

class F(AbstractLayer, AbstractSSS):

    def __init__(_s, id, pic, sh):
        AbstractLayer.__init__(_s)
        _s.id = id
        _s.sh = sh
        _s.pic = pic  # NOT SCALED

        _s.gi = deepcopy(sh.gi.fs_gi)

        # _s.sps_gi = sh.gi.sps_gi  # better do this at sp level

        AbstractSSS.__init__(_s, sh, id)

        _s.sps = {}  # filled with spark instances (not allowed to generate them from inside here).

        adf = 5

    def gen_scale_vector(_s):

        scale_ss = []
        return scale_ss

    def finish_info(_s, fs_gi):
        """This is written manually and adds/changes things in gi.
        Usually this function is run dynamically depending on coordinates of
        a parent layer at a certain frame. But not always.
        """

        # fs_gi['max_ri'] = np.max(_s.extent[:, 1])

        return fs_gi

    def set_ld_and_theta(_s):

        pos = np.random.random_integers(0, len(_s.gi['left_offsets']) - 1, 1)[0]

        '''Determine whether its only 2 fs (for testing)'''

        if P.NUM_FS == 2:
            ''' minimum. MAKES SURE THEY ARE DISTRIBUTED EVENLY WHEN ONLY 2
            Also left_offsets are -10, 10 and theta_offsets hardcoded in this case in info'''
            if _s.id[-1] == '0':
                pos = 0
            else:
                pos = 1

        _s.gi['ld'][0] = _s.gi['left_mid'] + _s.gi['left_offsets'][pos]  # random randint
        _s.gi['theta_loc'] = np.pi / 2 + _s.gi['theta_offsets'][pos]

        _s.gi['ld'][1] = 420

    def set_frame_stop_to_sp_max(_s):
        """Loop through sps and set max to frame_stop"""

        _max = 0
        for sp_id, sp in _s.sps.items():
            if sp.frame_ss[1] > _max:
                _max = sp.frame_ss[1]

        _s.frame_ss[1] = deepcopy(_max) + 5
