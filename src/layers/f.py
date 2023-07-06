

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

        if P.A_SPS:
            _s.sps_gi = sh.gi.sps_gi

        _s.zorder = _s.gi['zorder']

        AbstractSSS.__init__(_s, sh, id)

        _s.sps = {}  # filled with spark instances (not allowed to generate them from inside here).

        '''In N2 below is generated dynamically (probably because there may be some uncertainty regarding
        position of sh, but probably not necessary.'''

        _s.scale_vector = np.linspace(_s.gi['scale_ss'][0], _s.gi['scale_ss'][1], _s.gi['frames_tot'])  # USE GI
        _s.rotation_v = np.linspace(0.01, _s.gi['rad_rot'], num=len(_s.scale_vector))

        alpha_y_range = [0, 0.6]
        if P.POST:
            alpha_y_range = [0, 0.01]

        if 'alpha_y_range' in _s.gi:
            alpha_y_range = _s.gi['alpha_y_range']
        _s.alpha = gen_alpha(_s, frames_tot=_s.gi['frames_tot'], y_range=alpha_y_range)

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
