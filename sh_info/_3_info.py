import copy

from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np


class Sh_3_info(ShInfoAbstract):
    """
    Basically this is the json replacement (also chronicle to some extent).
    Just very basic stuff
    """

    def __init__(_s, pulse, top_point):
        super().__init__()
        _s.id = '3'
        _s.extent = "static"
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        # _s.frames_tot = _s.frame_ss[1] - _s.frame_ss[0]  # ONLY ONE WHO USES .
        _s.zorder = 110  # needed to set sp zorder using randint in dyn_gen

        _s.INIT_FRAME = 2  # used by all cs

        _s.ld = [top_point[0] + 0, top_point[1] + 0]
        _s.child_names = ['cs', 'srs', 'sps']  # both cks and cds

        if P.A_CS:  # THEY ALL HAVE INDIVIDUAL GI'S
            _s.cs_gi0 = _s.gen_cs_gi0(frames_tot=pulse[0] + 20, frames_tot1=200, z_d=8)
            _s.cs_gi1 = _s.gen_cs_gi1(frames_tot=pulse[0] + 70, frames_tot1=200, z_d=2)  # OBS 100 is volc_d
            _s.cs_gi2 = _s.gen_cs_gi2(frames_tot=pulse[0] + 30, frames_tot1=200, z_d=1)
            _s.cs_gi3 = _s.gen_cs_gi3(frames_tot=pulse[0] + 10, frames_tot1=200, z_d=3)
            # _s.cs_gi4 = _s.gen_cs_gi4(frames_tot=pulse[0] + 30, frames_tot1=300, z_d=1)
            # _s.cs_gi5 = _s.gen_cs_gi5(frames_tot=pulse[0] + 20, frames_tot1=200, z_d=7)
            # _s.cs_gi6 = _s.gen_cs_gi6(frames_tot=pulse[0] + 30, frames_tot1=300, z_d=5)
            # _s.cs_gi7 = _s.gen_cs_gi7(frames_tot=pulse[0] + 0, frames_tot1=500, z_d=7)
            # _s.cs_gi8 = _s.gen_cs_gi8(frames_tot=pulse[0] + 90, frames_tot1=500, z_d=8)
            _s.cs_gi9 = _s.gen_cs_gi9(frames_tot=pulse[0] + 80, frames_tot1=200, z_d=7)
            # _s.cs_gi10 = _s.gen_cs_gi10(frames_tot=pulse[0] + 100, frames_tot1=200, z_d=8)  # OBS 100 is volc_d
            # _s.cs_gi11 = _s.gen_cs_gi11(frames_tot=pulse[0] + 90, frames_tot1=600, z_d=-30)  # OBS 100 is volc_d
            # _s.cs_gi12 = _s.gen_cs_gi12(frames_tot=pulse[0] + 110, frames_tot1=450, z_d=-40)  # OBS 100 is volc_d

            aa = 5

        if P.A_SRS:  # different gis here have nothing to do with pic, but rather with init frames

            '''
            IF AN SR IS GENERATED HERE, ITS NUMBER MUST BE MATCHABLE WITH C NUMBER ABOVE. 
            SR PIC NUMBER IS IRRELEVANT. 
            INIT_FRAMES MUST BE UNIQUE. ALSO, ONCE ADDED, IT WILL BE PARSED IN MAIN, 
            AND WILL CRASH IF THERE IS NO CORRESPONDING C PIC'''
            init_frames = []

            '''THEY USE CORRESPONDING CS init_frames
            THESE COULD HAVE BEEN MERGED INTO A SINGLE GI BUT WHATEVER
            '''
            _s.srs_gi0, init_frames = _s.gen_srs_gi0(init_frames)  # THIS MEANS THERE MUST BE A '3_c_0'
            _s.srs_gi1, init_frames = _s.gen_srs_gi1(init_frames)
            _s.srs_gi2, init_frames = _s.gen_srs_gi2(init_frames)
            _s.srs_gi3, init_frames = _s.gen_srs_gi3(init_frames)
            # _s.srs_gi4, init_frames = _s.gen_srs_gi4(init_frames)
            # _s.srs_gi5, init_frames = _s.gen_srs_gi5(init_frames)  # perhaps redundant (???)
            # _s.srs_gi6, init_frames = _s.gen_srs_gi6(init_frames)
            # _s.srs_gi7, init_frames = _s.gen_srs_gi7(init_frames)
            # _s.srs_gi8, init_frames = _s.gen_srs_gi8(init_frames)
            _s.srs_gi9, init_frames = _s.gen_srs_gi9(init_frames)
            # _s.srs_gi10, init_frames = _s.gen_srs_gi10(init_frames)
            # _s.srs_gi11, init_frames = _s.gen_srs_gi11(init_frames)

            _s.srs_gi = {  # these numbers correspond to c!
                '0': _s.srs_gi0,
                '1': _s.srs_gi1,  # IF A C AND CORR SR EXISTS, THEN SO MUST THIS
                '2': _s.srs_gi2,
                '3': _s.srs_gi3,
                # '4': _s.srs_gi4,
                # '5': _s.srs_gi5,
                # '6': _s.srs_gi6,
                # '7': _s.srs_gi7,
                # '8': _s.srs_gi8,
                '9': _s.srs_gi9,
                # '10': _s.srs_gi10,
                # '11': _s.srs_gi11
            }

            init_frames.sort()
            _s.srs_gi_init_frames = init_frames
            _s.srs_gi_init_frames.sort()
            adf = 5

        if P.A_SRS and P.A_SPS:

            '''
            OBS sps_gi0 and sps_gi1 CAN BE CALLED BY ANY SH, SO NAME CANT BE CHANGED
            '''

            init_frames = []  # NEW: MUST BE UNIQUE. EACH GI ONLY HAS 1 INIT_FRAME, BUT THEY STILL CANT BE SAME.
            _s.sps_gi0, init_frames = _s.gen_sps_gi0(init_frames)  # THIS MEANS THERE MUST BE A '3_sr_0'
            _s.sps_gi1, init_frames = _s.gen_sps_gi1(init_frames)  # THIS MEANS THERE MUST BE A '3_sr_0'
            _s.sps_gi2, init_frames = _s.gen_sps_gi2(init_frames)  # THIS MEANS THERE MUST BE A '3_sr_2'
            _s.sps_gi3, init_frames = _s.gen_sps_gi3(init_frames)  # THIS MEANS THERE MUST BE A '3_sr_3'
            # _s.sps_gi4, init_frames = _s.gen_sps_gi4(init_frames)  # THIS MEANS THERE MUST BE A '3_sr_3'
            # _s.sps_gi5, init_frames = _s.gen_sps_gi5(init_frames)  # THIS MEANS THERE MUST BE A '3_sr_3'
            # _s.sps_gi6, init_frames = _s.gen_sps_gi6(init_frames)
            # _s.sps_gi7, init_frames = _s.gen_sps_gi7(init_frames)
            # _s.sps_gi8, init_frames = _s.gen_sps_gi8(init_frames)
            _s.sps_gi9, init_frames = _s.gen_sps_gi9(init_frames)
            # _s.sps_gi10, init_frames = _s.gen_sps_gi10(init_frames)
            # _s.sps_gi11, init_frames = _s.gen_sps_gi11(init_frames)

            _s.sps_gi_init_frames = init_frames
            _s.sps_gi_init_frames.sort()

            _s.sps_gi = {  # these numbers correspond to c!
                '0': _s.sps_gi0,
                '1': _s.sps_gi1,  # IF A C AND CORR SR EXISTS, THEN SO MUST THIS
                '2': _s.sps_gi2,  # IF A C AND CORR SR EXISTS, THEN SO MUST THIS
                '3': _s.sps_gi3,  # IF A C AND CORR SR EXISTS, THEN SO MUST THIS
                # '4': _s.sps_gi4,  # IF A C AND CORR SR EXISTS, THEN SO MUST THIS
                # '5': _s.sps_gi5,  # IF A C AND CORR SR EXISTS, THEN SO MUST THIS
                # '6': _s.sps_gi6,
                # '7': _s.sps_gi7,
                # '8': _s.sps_gi8,
                '9': _s.sps_gi9,
                # '10': _s.sps_gi10,
                # '11': _s.sps_gi11
            }

            '''Apply to all'''
            for sp_gi_key, sp_gi in _s.sps_gi.items():

                sp_gi['rgb_start'] = [0.4, 0.9]
                sp_gi['rgb_theta_diff_c'] = 1
                sp_gi['rgb_v_diff_c'] = 0.01
                sp_gi['alpha_y_range'] = [0.1, 0.8]

        else:
            _s.sps_gi_init_frames = []  # needed by animation loop

        adf = 6

    def gen_srs_init_frames(_s, _cs_gi, init_frames):

        """
        C used to gen init frames for sr
        """

        frames_tot = 1500
        clf = _cs_gi['init_frame'] + _cs_gi['frames_tot'] + _cs_gi['frames_tot1']  # c_last_frame
        # start = _cs_gi['init_frame'] + int(0.9 * (_cs_gi['frames_tot'] + _cs_gi['frames_tot1']))  # STUPIDO (too complex)
        start = clf + random.randint(-10, 300)
        if _cs_gi['id'] == 'c4':
            start = clf - 300
        stop = start + 50
        in_f_cand = list(range(start, stop, 3))  # so 1 launched every 6th frame, totalling 14
        in_f2 = []

        for fr in in_f_cand:
            if fr not in init_frames:
                in_f2.append(fr)
                init_frames.append(fr)
            else:
                fr_c2 = fr
                attempts = 0
                while True:
                    fr_c2 += 1
                    if fr_c2 not in init_frames:
                        in_f2.append(fr_c2)
                        init_frames.append(fr_c2)
                        break
                    else:
                        attempts += 1
                    if attempts > 1000:
                        raise Exception("> 1000 attempts.")

        in_f = in_f2

        return in_f, init_frames, frames_tot

    def gen_cs_gi0(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 0, _s.ld[1] - 10]

        if P.DEBUG:  # don't let coloring fool one, it does overwrite
            frames_tot = 10
            frames_tot1 = 20

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c0',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 40,
            'theta': 1.5,
            'r_f_d': 0.5,  # more = more up (for some weird reason)
            'extra_offset_x': 3,
            'extra_offset_y': -3,
            'up_down': 'up',
            'rad_rot': -2,
            'zorder': _s.zorder + z_d
        }

        # gi['init_frame'] = 2
        # gi['ld'] = [_s.ld[0] - 12, _s.ld[1] + 10]  # -6 TUNED WITH affine2D.translate!!!
        # gi['frames_tot'] = 10
        # gi['frames_tot1'] = 100
        #
        # if P.DEBUG:
        #     gi['frames_tot'] = 10
        #     gi['frames_tot1'] = 20
        #
        # '''OBS THIS HAS TO BE SECOND BEFORE SET_EXTENT, THEN SET TO FIRST'''
        # # gi['ld_ss'] = [[gi['ld'][0], gi['ld'][1]], [gi['ld'][0], gi['ld'][1]]]  # set extent needs this
        # gi['frame_ss'] = [gi['init_frame'], gi['init_frame'] + gi['frames_tot']]
        # gi['frame_ss'] = [gi['frame_ss'][1], gi['frame_ss'][1] + gi['frames_tot1']]
        # # gi['frame_ss1'] = [gi['frame_ss'][1], gi['frame_ss'][1] + 30]
        # gi['scale_ss'] = [1, 1]
        #
        # gi['v'] = 20
        # gi['theta'] = 0.8 * 2 * np.pi   # 2pi/4 is straight up, 2pi/8 is 45% to right   pos=left, neg=right
        # # gi['theta'] = np.pi + 0.001  # 2pi/4 is straight up, 2pi/8 is 45% to right
        # gi['r_f_d'] = 0.01  # THIS MESSES UP START POS
        # gi['extra_offset_x'] = 0
        # gi['extra_offset_y'] = 5
        # gi['up_down'] = 'up'
        #
        # gi['zorder'] = 110

        '''cd'''

        return gi

    def gen_srs_gi0(_s, init_frames):

        """
        OBS controls movement of ALL srs for a GIVEN c.
        NOT REPEATABLE
        """

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi0, init_frames=init_frames)

        assert(in_f[-1] < P.FRAMES_STOP)

        srs_gi = {
            'c_id': '3_c_0',
            'init_frames': in_f,
            'ld_offset_loc': [5, 0],  # OBS there is no ss, only start!
            'ld_offset_scale': [1, 3],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 150,  # rc=2
            'v_scale': 4,
            'scale_ss': [0.01, 3],
            'theta_loc': -0.5,  #0.6 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.0,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.00,
            'up_down': 'down',
            'alpha_y_range': [0.01, 0.2],
            'zorder': _s.cs_gi0['zorder']
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi, init_frames

    def gen_sps_gi0(_s, init_frames):

        """
        NEW: DEPEND ON CORRESPONDING SR INSTEAD OF C
        ONLY 1 init frame, but its in init_frames list
        """

        index = int(len(_s.srs_gi0['init_frames']) * 0.8)  # 0.8 is towards the end of sr init_frames
        init_frame = _s.cs_gi0['init_frame'] + _s.cs_gi0['frames_tot'] + 0.9 * _s.cs_gi0['frames_tot1']  # sr first frame
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '0',
            'c_id': '3_c_0',
            'frames_tot': 800,
            'init_frame_max_dist': 10,  # it is called but 0 so no diff
            'v_loc': 5, 'v_scale': 10,
            'theta_loc': -0.7, 'theta_scale': 0.3,
            'r_f_d_loc': 0.5, 'r_f_d_scale': 0.1,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [5, 1],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.5, 0.8], 'R_scale': 0.2,
            'G_ss': [0.35, 0.2], 'G_scale': 0.1,
            'B_ss': [0.15, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.zorder
        }

        return sps_gi, init_frames

    def gen_cs_gi1(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 50, _s.ld[1] + 40]

        if P.DEBUG:
            frames_tot = 10
            frames_tot1 = 30

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c1',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 40,
            'theta': -1.4,
            'r_f_d': 0.1,
            'extra_offset_x': -1,
            'extra_offset_y': 5,
            'up_down': 'up',
            'rad_rot': 1.,
            'zorder': _s.zorder + z_d
        }

        # gi['init_frame'] = 2
        # gi['ld'] = [_s.ld[0] - 50, _s.ld[1] + 40]  # -6 TUNED WITH affine2D.translate!!!
        # # gi['ld'] = [_s.ld[0] - 13, _s.ld[1] + 3]  # -6 TUNED WITH affine2D.translate!!!
        #
        # gi['frames_tot'] = 60
        # gi['frames_tot1'] = 210
        #
        # if P.DEBUG:
        #     gi['frames_tot'] = 30
        #     gi['frames_tot1'] = 50
        #
        # # frame_ss =
        #
        # '''OBS THIS HAS TO BE SECOND BEFORE SET_EXTENT, THEN SET TO FIRST'''
        # # gi['ld_ss'] = [[gi['ld'][0], gi['ld'][1]], [gi['ld'][0], gi['ld'][1]]]  # set extent needs this
        # gi['frame_ss'] = [gi['init_frame'], gi['init_frame'] + gi['frames_tot']]
        # gi['frame_ss'] = [gi['frame_ss'][1], gi['frame_ss'][1] + gi['frames_tot1']]
        # # gi['frame_ss1'] = [gi['frame_ss'][1], gi['frame_ss'][1] + 30]
        # gi['scale_ss'] = [1, 1]
        #
        # gi['v'] = 25
        # gi['theta'] = 0.8 * 2 * np.pi   # 2pi/4 is straight up, 2pi/8 is 45% to right   pos=left, neg=right
        # # gi['theta'] = np.pi + 0.001  # 2pi/4 is straight up, 2pi/8 is 45% to right
        # gi['r_f_d'] = 0.01  # THIS MESSES UP START POS
        # gi['extra_offset_x'] = 0
        # gi['extra_offset_y'] = 8
        # gi['up_down'] = 'up'
        # gi['zorder'] = 90

        '''cd'''

        return gi

    def gen_srs_gi1(_s, init_frames):

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi1, init_frames=init_frames)

        srs_gi = {
            'c_id': '3_c_1',
            'init_frames': in_f,
            'ld_offset_loc': [23, -20],  # OBS there is no ss, only start!
            'ld_offset_scale': [6, 2],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 150,  # rc=2
            'v_scale': 6,
            'scale_ss': [0.01, 3],
            'theta_loc': -0.6, #0.9 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.000,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.05,
            'up_down': 'down',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.cs_gi1['zorder']
        }

        return srs_gi, init_frames

    def gen_sps_gi1(_s, init_frames):

        index = int(len(_s.srs_gi1['init_frames']) * 0.8)  # 0.8 is towards the end of sr init_frames
        init_frame = _s.cs_gi1['init_frame'] + _s.cs_gi1['frames_tot'] + 0.9 * _s.cs_gi1['frames_tot1']
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '1',
            'c_id': '3_c_1',
            'frames_tot': 800,
            'init_frame_max_dist': 10,  #
            'v_loc': 5, 'v_scale': 5,
            'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
            'theta_loc': -0.9, 'theta_scale': 0.1,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [5, -10],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.9, 1], 'R_scale': 0,
            'G_ss': [0.5, 0.01], 'G_scale': 0.1,
            'B_ss': [0.01, 0.01], 'B_scale': 0,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.zorder
        }

        return sps_gi, init_frames

    def gen_cs_gi2(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 40, _s.ld[1] + 25]

        if P.DEBUG:
            frames_tot = 20
            frames_tot1 = 30

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c2',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 30,
            'theta': 2,
            'r_f_d': 0.1,
            'extra_offset_x': 0,
            'extra_offset_y': 0,
            'up_down': 'up',
            'rad_rot': -2.5,
            'zorder': _s.zorder + z_d
        }

        # gi['init_frame'] = 2
        # gi['ld'] = [_s.ld[0] - 40, _s.ld[1] + 30]  # -6 TUNED WITH affine2D.translate!!!
        # # gi['ld'] = [_s.ld[0] - 13, _s.ld[1] + 3]  # -6 TUNED WITH affine2D.translate!!!
        #
        # gi['frames_tot'] = 30
        # gi['frames_tot1'] = 200
        #
        # if P.DEBUG:
        #     gi['frames_tot'] = 20
        #     gi['frames_tot1'] = 40
        #
        # '''OBS THIS HAS TO BE SECOND BEFORE SET_EXTENT, THEN SET TO FIRST'''
        # gi['ld_ss'] = [[gi['ld'][0], gi['ld'][1]], [gi['ld'][0], gi['ld'][1]]]  # set extent needs this
        # gi['frame_ss'] = [gi['init_frame'], gi['init_frame'] + gi['frames_tot']]
        # gi['frame_ss'] = [gi['frame_ss'][1], gi['frame_ss'][1] + gi['frames_tot1']]
        # # gi['frame_ss1'] = [gi['frame_ss'][1], gi['frame_ss'][1] + 30]
        # gi['scale_ss'] = [1, 1]
        #
        # gi['v'] = 15
        # gi['theta'] = 0.8 * 2 * np.pi   # 2pi/4 is straight up, 2pi/8 is 45% to right   pos=left, neg=right
        # # gi['theta'] = np.pi + 0.001  # 2pi/4 is straight up, 2pi/8 is 45% to right
        # gi['r_f_d'] = 0.01  # THIS MESSES UP START POS
        # gi['extra_offset_x'] = 0
        # gi['extra_offset_y'] = 8
        # gi['up_down'] = 'up'
        #
        # gi['zorder'] = 90

        '''cd'''

        return gi

    def gen_srs_gi2(_s, init_frames):

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi2, init_frames=init_frames)

        srs_gi = {
            'c_id': '3_c_2',
            'init_frames': in_f,
            'ld_offset_loc': [23, -10],  # OBS there is no ss, only start!
            'ld_offset_scale': [6, 2],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 150,  # rc=2
            'v_scale': 6,
            'scale_ss': [0.01, 3],
            'theta_loc': -0.7, #0.9 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.000,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.05,
            'up_down': 'down',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.cs_gi2['zorder']
        }

        return srs_gi, init_frames

    def gen_sps_gi2(_s, init_frames):

        index = int(len(_s.srs_gi2['init_frames']) * 0.8)  # 0.8 is towards the end of sr init_frames
        init_frame = _s.cs_gi2['init_frame'] + _s.cs_gi2['frames_tot'] + 0.9 * _s.cs_gi2['frames_tot1']
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '2',
            'c_id': '3_c_2',
            'frames_tot': 800,
            'init_frame_max_dist': 10,  #
            'v_loc': 5, 'v_scale': 10,
            'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
            'theta_loc': -0.3, 'theta_scale': 0.3,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [10, -3],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.9, 1], 'R_scale': 0,
            'G_ss': [0.5, 0.01], 'G_scale': 0.1,
            'B_ss': [0.01, 0.01], 'B_scale': 0,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.zorder
        }

        return sps_gi, init_frames

    def gen_cs_gi3(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 10, _s.ld[1] - 5]

        if P.DEBUG:
            frames_tot = 30
            frames_tot1 = 20

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c3',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 30,
            'theta': 2,
            'r_f_d': 0.1,
            'extra_offset_x': 0,
            'extra_offset_y': 0,
            'up_down': 'up',
            'rad_rot': -1.5,
            'zorder': _s.zorder + z_d
        }

        if P.POST:
            gi['v'] = 70

        return gi

    def gen_srs_gi3(_s, init_frames):

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi3, init_frames=init_frames)

        srs_gi = {
            'c_id': '3_c_3',
            'init_frames': in_f,
            'ld_offset_loc': [5, -5],  # OBS there is no ss, only start!
            'ld_offset_scale': [2, 2],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 140,  # rc=2
            'v_scale': 6,
            'scale_ss': [0.01, 4],
            'theta_loc': -0.5,  # 0.9 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.000,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.05,
            'up_down': 'down',
            'alpha_y_range': [0.0, 0.15],
            'zorder': _s.cs_gi3['zorder']
        }

        return srs_gi, init_frames

    def gen_sps_gi3(_s, init_frames):

        index = int(len(_s.srs_gi3['init_frames']) * 0.8)  # 0.8 is towards the end of sr init_frames
        init_frame = _s.cs_gi3['init_frame'] + _s.cs_gi3['frames_tot'] + 0.9 * _s.cs_gi3['frames_tot1']
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '3',
            'c_id': '3_c_3',
            'frames_tot': 800,
            'init_frame_max_dist': 10,  #
            'v_loc': 5, 'v_scale': 12,
            'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
            'theta_loc': -0.3, 'theta_scale': 0.3,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [10, -3],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.9, 1], 'R_scale': 0,
            'G_ss': [0.5, 0.01], 'G_scale': 0.1,
            'B_ss': [0.01, 0.01], 'B_scale': 0,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.zorder
        }

        return sps_gi, init_frames

    def gen_cs_gi4(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 22, _s.ld[1] + 7]

        if P.DEBUG:
            frames_tot = 20
            frames_tot1 = 40

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c4',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 25,
            'theta': 2,
            'r_f_d': 0.1,
            'extra_offset_x': -3,
            'extra_offset_y': -2,
            'up_down': 'up',
            'rad_rot': -1.8,
            'zorder': _s.zorder + z_d
        }

        return gi

    def gen_srs_gi4(_s, init_frames): # COVERS UGLY 7

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi4, init_frames=init_frames)

        srs_gi = {
            'c_id': '3_c_4',
            'init_frames': in_f,
            'ld_offset_loc': [3, -2],  # OBS there is no ss, only start!
            'ld_offset_scale': [3, 5],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 150,  # rc=2
            'v_scale': 6,
            'scale_ss': [0.01, 3],
            'theta_loc': -0.3,  # 0.9 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.1,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.05,
            'up_down': 'down',
            'alpha_y_range': [0.01, 0.2],
            'zorder': _s.cs_gi7['zorder'] + 1
        }

        return srs_gi, init_frames

    def gen_sps_gi4(_s, init_frames):

        # index = int(len(_s.srs_gi4['init_frames']) * 0.8)  # 0.8 is towards the end of sr init_frames
        init_frame = _s.cs_gi4['init_frame'] + _s.cs_gi4['frames_tot'] + 0.9 * _s.cs_gi4['frames_tot1']
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '4',
            'c_id': '3_c_4',
            'frames_tot': 800,
            'init_frame_max_dist': 10,  #
            'v_loc': 5, 'v_scale': 10,
            'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
            'theta_loc': -1.6, 'theta_scale': 0.3,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [10, -3],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.9, 1], 'R_scale': 0,
            'G_ss': [0.5, 0.01], 'G_scale': 0.1,
            'B_ss': [0.01, 0.01], 'B_scale': 0,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.zorder
        }

        return sps_gi, init_frames

    def gen_cs_gi5(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 13, _s.ld[1] + 0]

        if P.DEBUG:
            frames_tot = 10
            frames_tot1 = 20

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c5',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 25,
            'theta': -1.5,
            'r_f_d': 0.1,
            'extra_offset_x': 0,
            'extra_offset_y': 0,
            'up_down': 'up',
            'rad_rot': -1.5,
            'zorder': _s.zorder + z_d
        }

        return gi

    def gen_srs_gi5(_s, init_frames):

        """
        OBS controls movement of ALL srs for a GIVEN c.
        NOT REPEATABLE
        """

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi5, init_frames=init_frames)

        assert(in_f[-1] < P.FRAMES_STOP)

        srs_gi = {
            'c_id': '3_c_5',
            'init_frames': in_f,
            'ld_offset_loc': [-5, -5],  # OBS there is no ss, only start!
            'ld_offset_scale': [3, 1],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 150,  # rc=2
            'v_scale': 10,
            'scale_ss': [0.01, 3],
            'theta_loc': -1.2,  #0.6 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.1,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.00,
            'up_down': 'down',
            'alpha_y_range': [0, 0.15],
            'zorder': _s.cs_gi5['zorder']
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi, init_frames

    def gen_sps_gi5(_s, init_frames):

        # index = int(len(_s.srs_gi5['init_frames']) * 0.8)  # 0.8 is towards the end of sr init_frames
        init_frame = _s.cs_gi5['init_frame'] + _s.cs_gi5['frames_tot'] + 0.9 * _s.cs_gi5['frames_tot1'] + 3
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '5',
            'c_id': '3_c_5',
            'frames_tot': 600,
            'init_frame_max_dist': 10,  #
            'v_loc': 5, 'v_scale': 4,
            'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
            'theta_loc': 0.3, 'theta_scale': 0.3,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [10, -3],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 2],
            'R_ss': [0.9, 1], 'R_scale': 0,
            'G_ss': [0.5, 0.01], 'G_scale': 0.1,
            'B_ss': [0.01, 0.01], 'B_scale': 0,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.zorder
        }

        return sps_gi, init_frames

    def gen_cs_gi6(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 10, _s.ld[1] - 2]

        if P.DEBUG:
            frames_tot = 10
            frames_tot1 = 30

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c6',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 40,
            'theta': -1.4,
            'r_f_d': 0.01,
            'extra_offset_x': 0,
            'extra_offset_y': 2,
            'up_down': 'up',
            'rad_rot': -0.9,
            'zorder': _s.zorder + z_d
        }

        return gi

    def gen_srs_gi6(_s, init_frames):

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi6, init_frames=init_frames)

        srs_gi = {
            'c_id': '3_c_6',
            'init_frames': in_f,
            'ld_offset_loc': [5, -5],  # OBS there is no ss, only start!
            'ld_offset_scale': [2, 2],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 160,  # rc=2
            'v_scale': 6,
            'scale_ss': [0.01, 3],
            'theta_loc': -0.5,  # 0.9 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.000,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.05,
            'up_down': 'down',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.cs_gi6['zorder']
        }

        return srs_gi, init_frames

    def gen_sps_gi6(_s, init_frames):

        # index = int(len(_s.srs_gi6['init_frames']) * 0.8)  # 0.8 is towards the end of sr init_frames
        init_frame = _s.cs_gi6['init_frame'] + _s.cs_gi6['frames_tot'] + 0.9 * _s.cs_gi6['frames_tot1'] + 3
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '6',
            'c_id': '3_c_6',
            'frames_tot': 900,
            'init_frame_max_dist': 30,  #
            'v_loc': 10, 'v_scale': 10,
            'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
            'theta_loc': -0.3, 'theta_scale': 0.3,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [10, -3],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.9, 1], 'R_scale': 0,
            'G_ss': [0.5, 0.01], 'G_scale': 0.1,
            'B_ss': [0.01, 0.01], 'B_scale': 0,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.zorder
        }

        return sps_gi, init_frames

    def gen_cs_gi7(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 25, _s.ld[1] + 10]

        # if P.DEBUG:
        #     frames_tot = 10
        #     frames_tot1 = 30

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c7',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 28,
            'theta': 1.7,
            'r_f_d': 0.2,
            'extra_offset_x': 0,
            'extra_offset_y': 6,
            'up_down': 'up',
            'rad_rot': 0.4,
            'zorder': _s.zorder + z_d
        }

        return gi

    def gen_srs_gi7(_s, init_frames):

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi7, init_frames=init_frames)

        srs_gi = {
            'c_id': '3_c_7',
            'init_frames': in_f,
            'ld_offset_loc': [5, -5],  # OBS there is no ss, only start!
            'ld_offset_scale': [2, 2],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 140,  # rc=2
            'v_scale': 10,
            'scale_ss': [0.01, 3],
            'theta_loc': -0.5,  # 0.9 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.000,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.05,
            'up_down': 'down',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.cs_gi7['zorder'] + 10
        }

        return srs_gi, init_frames

    def gen_sps_gi7(_s, init_frames):

        """
        """

        # index = int(len(_s.srs_gi7['init_frames']) * 0.8)  # 0.8 is towards the end of sr init_frames
        init_frame = _s.cs_gi7['init_frame'] + _s.cs_gi7['frames_tot'] + 0.9 * _s.cs_gi7['frames_tot1']
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '7',
            'c_id': '3_c_7',
            'frames_tot': 800,
            'init_frame_max_dist': 10,  # it is called but 0 so no diff
            'v_loc': 5, 'v_scale': 10,
            'theta_loc': -0.7, 'theta_scale': 0.3,
            'r_f_d_loc': 0.9, 'r_f_d_scale': 0.1,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [5, 1],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.5, 0.8], 'R_scale': 0.2,
            'G_ss': [0.35, 0.2], 'G_scale': 0.1,
            'B_ss': [0.15, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.cs_gi7['zorder']
        }

        return sps_gi, init_frames

    def gen_cs_gi8(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 10, _s.ld[1] + 6]

        if P.DEBUG:
            frames_tot = 10
            frames_tot1 = 30

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c8',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 45,  # 83: 50
            'theta': 1.5,  # 83: 1.6
            'r_f_d': 0.7,
            'extra_offset_x': -5,
            'extra_offset_y': 0,
            'up_down': 'up',
            'rad_rot': 2.5,
            'zorder': _s.zorder + z_d
        }

        return gi

    def gen_srs_gi8(_s, init_frames):

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi8, init_frames=init_frames)

        srs_gi = {
            'c_id': '3_c_8',
            'init_frames': in_f,
            'ld_offset_loc': [0, -10],  # OBS there is no ss, only start!
            'ld_offset_scale': [2, 2],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 160,  # rc=2
            'v_scale': 6,
            'scale_ss': [0.01, 3],
            'theta_loc': -0.5,  # 0.9 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.000,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.05,
            'up_down': 'down',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.cs_gi8['zorder']
        }

        return srs_gi, init_frames

    def gen_sps_gi8(_s, init_frames):

        """
        """

        init_frame = _s.cs_gi8['init_frame'] + _s.cs_gi8['frames_tot'] + 0.9 * _s.cs_gi8['frames_tot1']
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '8',
            'c_id': '3_c_8',
            'frames_tot': 1200,
            'init_frame_max_dist': 10,  # it is called but 0 so no diff
            'v_loc': 5, 'v_scale': 12,
            'theta_loc': -0.7, 'theta_scale': 0.3,
            'r_f_d_loc': 0.9, 'r_f_d_scale': 0.1,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [5, 1],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.5, 0.8], 'R_scale': 0.2,
            'G_ss': [0.35, 0.2], 'G_scale': 0.1,
            'B_ss': [0.15, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.cs_gi8['zorder']
        }

        return sps_gi, init_frames

    def gen_cs_gi9(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 10, _s.ld[1] + 12]

        if P.DEBUG:
            frames_tot = 10
            frames_tot1 = 30

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c9',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 50,
            'theta': -1.8,
            'r_f_d': 0.1,
            'extra_offset_x': -2,
            'extra_offset_y': 5,
            'up_down': 'up',
            'rad_rot': 7.8,
            'zorder': _s.zorder + z_d
        }

        return gi

    def gen_srs_gi9(_s, init_frames):

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi9, init_frames=init_frames)

        srs_gi = {
            'c_id': '3_c_9',
            'init_frames': in_f,
            'ld_offset_loc': [0, 0],  # OBS there is no ss, only start!
            'ld_offset_scale': [2, 2],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 170,  # rc=2
            'v_scale': 15,
            'scale_ss': [0.01, 3],
            'theta_loc': -0.5,  # 0.9 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.000,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.05,
            'up_down': 'down',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.cs_gi9['zorder']
        }

        return srs_gi, init_frames

    def gen_sps_gi9(_s, init_frames):

        """
        """

        init_frame = _s.cs_gi9['init_frame'] + _s.cs_gi9['frames_tot'] + 0.9 * _s.cs_gi9['frames_tot1']
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '9',
            'c_id': '3_c_9',
            'frames_tot': 800,
            'init_frame_max_dist': 10,  # it is called but 0 so no diff
            'v_loc': 5, 'v_scale': 10,
            'theta_loc': 0.7, 'theta_scale': 0.3,
            'r_f_d_loc': 0.9, 'r_f_d_scale': 0.1,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [5, 1],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.5, 0.8], 'R_scale': 0.2,
            'G_ss': [0.35, 0.2], 'G_scale': 0.1,
            'B_ss': [0.15, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.cs_gi9['zorder']
        }

        return sps_gi, init_frames

    def gen_cs_gi10(_s, frames_tot, frames_tot1, z_d):
        ld = [_s.ld[0] + 11, _s.ld[1] + 14]

        if P.DEBUG:
            frames_tot = 10
            frames_tot1 = 30

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c10',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 20,
            'theta': -1.8,
            'r_f_d': 0.1,
            'extra_offset_x': 0,
            'extra_offset_y': 5,
            'up_down': 'up',
            'rad_rot': 0.5,
            'zorder': _s.zorder + z_d
        }

        return gi

    def gen_srs_gi10(_s, init_frames):

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi10, init_frames=init_frames)

        srs_gi = {
            'c_id': '3_c_10',
            'init_frames': in_f,
            'ld_offset_loc': [10, -10],  # OBS there is no ss, only start!
            'ld_offset_scale': [2, 2],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 170,  # rc=2
            'v_scale': 10,
            'scale_ss': [0.01, 4],
            'theta_loc': -0.5,  # 0.9 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.000,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.05,
            'up_down': 'down',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.cs_gi10['zorder']
        }

        return srs_gi, init_frames

    def gen_sps_gi10(_s, init_frames):

        """
        """

        init_frame = _s.cs_gi10['init_frame'] + _s.cs_gi10['frames_tot'] + 0.9 * _s.cs_gi10['frames_tot1']
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '10',
            'c_id': '3_c_10',
            'frames_tot': 800,
            'init_frame_max_dist': 10,  # it is called but 0 so no diff
            'v_loc': 5, 'v_scale': 10,
            'theta_loc': 0.7, 'theta_scale': 0.3,
            'r_f_d_loc': 0.9, 'r_f_d_scale': 0.1,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [5, 1],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.5, 0.8], 'R_scale': 0.2,
            'G_ss': [0.35, 0.2], 'G_scale': 0.1,
            'B_ss': [0.15, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': _s.cs_gi10['zorder']
        }

        return sps_gi, init_frames

    def gen_cs_gi11(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 15, _s.ld[1] + 20]

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c11',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 45,
            'theta': -1.7,
            'r_f_d': 0.6,
            'extra_offset_x': 8,
            'extra_offset_y': -3,
            'up_down': 'up',
            'rad_rot': 3.6,
            'zorder': _s.zorder + z_d
        }

        return gi

    def gen_srs_gi11(_s, init_frames):

        in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi11, init_frames=init_frames)

        srs_gi = {
            'c_id': '3_c_11',
            'init_frames': in_f,
            'ld_offset_loc': [10, -10],  # OBS there is no ss, only start!
            'ld_offset_scale': [2, 2],  # OBS there is no ss, only start!
            'frames_tot': frames_tot,
            'v_loc': 160,  # rc=2
            'v_scale': 10,
            'scale_ss': [0.01, 2],
            'theta_loc': -0.5,  # 0.9 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.000,
            'rad_rot': -2,
            'r_f_d_loc': 0.5,
            'r_f_d_scale': 0.05,
            'up_down': 'down',
            'alpha_y_range': [0, 0.2],
            'zorder': 125
        }

        return srs_gi, init_frames

    def gen_sps_gi11(_s, init_frames):

        """
        """

        init_frame = _s.cs_gi11['init_frame'] + _s.cs_gi11['frames_tot'] + 0.9 * _s.cs_gi11['frames_tot1']
        if init_frame in init_frames:
            raise Exception("cs sp init_frame already exists. Change frames_tot1 of c0")

        init_frames.append(init_frame)

        sps_gi = {
            'init_frames': [init_frame],
            'gi_id': '11',
            'c_id': '3_c_11',
            'frames_tot': 800,
            'init_frame_max_dist': 10,  # it is called but 0 so no diff
            'v_loc': 5, 'v_scale': 10,
            'theta_loc': 0.7, 'theta_scale': 0.3,
            'r_f_d_loc': 0.9, 'r_f_d_scale': 0.1,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 3, 'sp_len_scale': 8,
            'ld_offset_loc': [5, 1],  # this is wrt to ld, which is toward end of c path
            'ld_offset_scale': [1, 1],
            'R_ss': [0.5, 0.8], 'R_scale': 0.2,
            'G_ss': [0.35, 0.2], 'G_scale': 0.1,
            'B_ss': [0.15, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'up_down': 'up',
            'zorder': 120
        }

        return sps_gi, init_frames

    def gen_cs_gi12(_s, frames_tot, frames_tot1, z_d):

        ld = [_s.ld[0] - 25, _s.ld[1] + 50]

        if P.DEBUG:
            frames_tot = 10
            frames_tot1 = 30

        frame_ss = [_s.INIT_FRAME + frames_tot, _s.INIT_FRAME + frames_tot + frames_tot1]

        gi = {
            'id': 'c12',
            'init_frame': _s.INIT_FRAME,
            'ld': ld,
            'frames_tot': frames_tot,
            'frames_tot1': frames_tot1,
            'frame_ss': frame_ss,
            'scale_ss': [1, 1],
            'v': 40,
            'theta': 1.65,
            'r_f_d': 0.8,
            'extra_offset_x': 0,
            'extra_offset_y': -3,
            'up_down': 'up',
            'rad_rot': -1.1,
            'zorder': _s.zorder + z_d
        }

        return gi