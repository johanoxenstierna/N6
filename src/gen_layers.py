import os
import json
import numpy as np
from src.load_pics import load_pics
from src.genesis import init_infos
import P as P
from src.layers.sh import Sh
from src.layers.f import F
from src.layers.sp import Sp



class GenLayers:

    """
    OBS this time it's only the background that is being ax.shown here. The other ax objects are added and
    deleted within the animation loop to save CPU-time.
    Each pic is tied to exactly 1 class instance and that class instance takes info from either sh parent
    or other.
    """

    def __init__(_s):
        _s.pics = load_pics()
        _s.sh_gis = init_infos()
        _s.PATH_IMAGES = './images/processed/'
        # _s.ch = ch

    def gen_backgr(_s, ax0, axs0, axs1):

        if P.ARS == 0:  # shouldnt matter whether added to axs0 or axs1
            axs1.append(ax0.imshow(_s.pics['backgr_d'], zorder=1, alpha=1))  # index 0
        else:
            axs1.append(ax0.imshow(_s.pics['backgr_ars'], zorder=2, alpha=1))  # index 1

        ax0.axis([0, P.MAP_DIMS[0], P.MAP_DIMS[1], 0])
            # ax.axis([-30, 254, 133, -30])
            # ax.axis([0, 214, 0, 181])
            # ax.axis([0, 214, 181, 0])
            # ax.axis([0, 571, 0, 500])
        # else:
        #     ax.axis([0, 1280, 0, 720])
        # ax.invert_yaxis()  # ONLY IF SHIPS?
        # ax.grid()
        ax0.axis('off')  # TURN ON FOR FINAL

    def gen_shs(_s, ax, axs0):
        """
        Base objects (ships but they may not always be ships).
        """
        shs = {}
        for sh_id in P.SHS_TO_SHOW:  # number_id
            sh_gi = _s.sh_gis[sh_id]
            shs[sh_id] = Sh(pic=None, gi=sh_gi)  # No pic CURRENTLY

        return shs

    def gen_fs(_s, ax, axs0, shs):

        """FS"""
        for sh_id, sh in shs.items():
            if 'fs' in sh.gi.child_names:
                fs_pics = _s.pics['sh'][sh_id]['fs']
                sp_id_int = 0  # since there may be multiple f
                for pic_key, pic in fs_pics.items():
                    f = F(id=pic_key, pic=pic, sh=sh)  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?

                    f.set_ld_and_theta()
                    '''sps always generated, but they will not be animated
                    if A_SPS set to 0. If an sh has an f, '''

                    if P.A_SPS:
                        num_sp_f = P.NUM_SPS_F
                        for _ in range(num_sp_f):
                            sp_id_int += 1
                            sp = Sp(sh, sp_id_int, f)
                            sh.sps[sp.id] = sp
                            f.sps[sp.id] = sp  # why not use both

                    sh.fs[pic_key] = f

        return shs
