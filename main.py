"""
Sh are needed because it might be useful to
have different settings for different fs

"""

import numpy as np
import random
random.seed(7)  # ONLY HERE
np.random.seed(7)  # ONLY HERE
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from src import gen_layers
from src.ani_helpers import *
import P as P

WRITE = 0  # FIX: smoka frames, waves  # change IMMEDIATELY back to zero (it immediately kills old file when re-run)
FPS = 40

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, metadata=dict(artist='Me'), bitrate=3600)

fig, ax0 = plt.subplots(figsize=(10, 6))   # pic  214 181

im_ax = []
g = gen_layers.GenLayers()
g.gen_backgr(ax0, im_ax)

shs = g.gen_shs(ax0, im_ax)

if P.A_FS:
    shs = g.gen_fs(ax0, im_ax, shs)

if P.A_SPS:
    shs = g.gen_sps(ax0, im_ax, shs)  # OBS children of fs NOT GENERATED HERE

# li_pointer = None
'''VIEWER ==========================================='''
brkpoint = 4

def init():
    return im_ax


def animate(i):

    li_pointer = None
    # if P.A_LIS and '1' in shs.keys():
    #     if i in shs['1'].gi.lis_gi['init_frames']:
    #         pass
    #         # im_ax[2].set_alpha(0.1)

    prints = "i: " + str(i) + "  len_im_ax: " + str(len(im_ax))
    for sh_id, sh in shs.items():

        if i == 108:
            aaa = 5

        if P.A_FS and 'fs' in sh.gi.child_names:  # 0, 5, 6!!!
            if i in sh.gi.fs_gi['init_frames']:

                f = sh.find_free_obj(type='f')
                if f != None:
                    prints += "  adding f"
                    exceeds_frame_max, how_many = f.check_frame_max(i, f.gi['frames_tot'])
                    if exceeds_frame_max == True:
                        print("EXCEEDS MAX\n")
                        f.gi['frames_tot'] = how_many

                    f.drawn = 1  # this variable can serve multiple purposes (see below, and in set_clock)
                    sh.f_latest_drawn_id = f.id
                    f.set_frame_ss(i, f.gi['frames_tot'], dynamic=False)  # uses AbstractSSS

                    ''' EVIL BUG HERE. An F cannot be allowed to init new sp children if old children
                    are still being drawn!!! THIS MEANS F FRAMES_TOT MUST > SP FRAMES TOT'''
                    if P.A_SPS and sh.id not in ['1']:  # ? on second condition
                        for sp_key, sp in f.sps.items():
                            assert(sp.f != None)
                            sp.dyn_gen(i)  # YES KEEP THIS: there are thousands of sp and pre-storing xy for all is a bit crazy.
                            sp.drawn = 1
                            prints += "  adding sp"
                            sp.set_frame_ss(i, sp.gi['frames_tot'], dynamic=False)

                        # adf = 5
                else:
                    prints += "  no free f"

            for f_id, f in sh.fs.items():

                if f.drawn != 0:  # OBS the 4 from above is needed only the very first iteration it becomes visible
                    f.set_clock(i)

                    drawBool, index_removed = f.ani_update_step(ax0, im_ax)
                    if drawBool == 0:  # dont draw
                        continue
                    elif drawBool == 1:
                        mpl_affine(i, f, ax0, im_ax)
                        im_ax[f.index_im_ax].set_alpha(f.alpha[f.clock])
                    elif drawBool == 2:  # remove
                        prints += "  removing f"
                        decrement_all_index_im_ax(index_removed, shs)

                for sp_id, sp in f.sps.items():  # CHILD OF f
                    assert(sp.f != None)
                    if sp.drawn != 0:
                        sp.set_clock(i)
                        drawBoolSP, index_removed = sp.ani_update_step(ax0, im_ax, sp=True)
                        if drawBoolSP == 0:
                            continue
                        elif drawBoolSP == 1:
                            set_sps(sp, im_ax)

                        elif drawBoolSP == 2:
                            prints += "  removing sp"
                            decrement_all_index_im_ax(index_removed, shs)

        if P.A_SPS and 'sps' in sh.gi.child_names:  # SH sps  # 2, 3, 4, 7
            '''NOT f. OBS MULTIPLE DRAWS AT SAME FRAME ALLOWED HERE
            THIS IS NOT THERE FOR OTHERS'''
            # if i in sh.gi.sps_gi_init_frames:
            #     '''
            #     DECIDE WHICH GI TO USE
            #     This sets an init frame for the sp IN THE FUTURE
            #     Tries 50 times to find a free sp and if it finds one it gets drawn
            #     according to gi conditions.
            #     '''
            #
            #     if sh.id[0] in ['2', '4']:
            #         num = P.NUM_SPS_PER_L  # per L
            #     elif sh.id[0] in ['3']:
            #         num = P.NUM_SPS_PER_C  # '3'  (0 uses F)
            #     elif sh.id[0] in ['7']:
            #         num = P.NUM_SPS_PER_7
            #     prints += "  trying to add " + str(num) + "sp"
            #     # num_failed_to_add = 0
            #     for _ in range(num):  # will crash if no num
            #         sp = sh.find_free_obj(type='sp')
            #         if sp != None:
            #             assert (sp.f == None)  #
            #             sh.dyn_gen_child_sp(i, sp)  # assigns gi according to frame
            #         else:
            #             prints += "  COULDNT add sp"

            # DECIDE FRAME_SS. HERE FRAME_SS IS THE SAME FOR EVERY SP HERE
            for sp_id, sp in sh.sps.items():

                try:
                    _ = sp.init_frame
                except:
                    sp.init_frame = -999

                if sp.init_frame == i:  # only for sh sp
                    sp.drawn = 1
                    sp.set_frame_ss(i, len(sp.xy), dynamic=False)  # THIS SETS FRAME_SS

            # USUAL SET_DATA
            for sp_id, sp in sh.sps.items():
                if sp.drawn != 0 and sp.f == None:
                    sp.set_clock(i)
                    drawBool, index_removed = sp.ani_update_step(ax0, im_ax, sp=True)
                    if drawBool == 0:
                        continue
                    elif drawBool == 1:
                        set_sps(sp, im_ax)
                        # im_ax[sp.index_im_ax].set_alpha(1)

                    elif drawBool == 2:
                        decrement_all_index_im_ax(index_removed, shs)
                        continue


        print(prints)

    return im_ax  # if run live, it runs until window is closed


sec_vid = ((P.FRAMES_STOP - P.FRAMES_START) / FPS)
min_vid = ((P.FRAMES_STOP - P.FRAMES_START) / FPS) / 60
print("len of vid: " + str(sec_vid) + " s" + "    " + str(min_vid) + " min")

start_t = time.time()
ani = animation.FuncAnimation(fig, animate, frames=range(P.FRAMES_START, P.FRAMES_STOP),
                              blit=True, interval=1, init_func=init,
                              repeat=False)  # interval only affects live ani. blitting seems to make it crash

if WRITE == 0:
    # pass
    plt.show()
else:
    ani.save('./vids/vid_' + str(WRITE) + '.mp4', writer=writer)

tot_time = round((time.time() - start_t) / 60, 4)
print("minutes to make animation: " + str(tot_time) + " |  min_gen/min_vid: " + str(tot_time / min_vid))  #
