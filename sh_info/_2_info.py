"""the centre of the flame"""

from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np
import copy

class Sh_2_info(ShInfoAbstract):

    """
    Basically this is the json replacement (also chronicle to some extent).
    Just very basic stuff
    """

    def __init__(_s, START_F, EXPL_F, top_point):
        super().__init__()
        _s.id = '2'
        _s.extent = "static"
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        _s.frames_tot = _s.frame_ss[1] - _s.frame_ss[0]  # l frames_tot set below

        _s.ld = top_point
        # _s.child_names = ['sps', 'ls', 'rs', 'srs']
        _s.child_names = ['sps', 'ls', 'srs']

        '''THIS IS SHIT: Basically they will only be plotted once so they will be unavailable for 99% of init_frames, 
        but sps plotted a bunch.
        NEW: Only plotted once and sps controlled with init_frame_max_dist and num_scale
        '''
        _s.zorder = 200
        _s.ls_gi = _s.gen_ls_gi(START_F, EXPL_F)  # NO DYN_GEN


        if P.A_SPS:

            '''
            TODO distribute these between them based on pulse. 
            TODO2: add num sp to generate (50 in main) whenever init frame hit
            L needs to be generated based on these. 
            '''

            # sps_init_frames = []
            # _s.sps_gi0, sps_init_frames = _s.gen_sps_gi0(sps_init_frames)
            # _s.sps_gi1, sps_init_frames = _s.gen_sps_gi1(sps_init_frames)\

            _s.sps_gi0 = _s.gen_sps_gi0(frames_tot=200)
            _s.sps_gi1 = _s.gen_sps_gi1(frames_tot=350)
            _s.sps_gi2 = _s.gen_sps_gi2(frames_tot=350)
            _s.sps_gi3 = _s.gen_sps_gi3(frames_tot=350)
            _s.sps_gi4 = _s.gen_sps_gi4(frames_tot=350)

            _s.sps_gi = {
                '0': _s.sps_gi0,
                '1': _s.sps_gi1,
                '2': _s.sps_gi2,
                '3': _s.sps_gi3,
                '4': _s.sps_gi4
            }

            _s.extend_sps_init_frames(EXTEND_PARAM=50)

            _s.sps_gi0['init_frames'] = [x for x in _s.sps_gi0['init_frames'] if x < EXPL_F - 50]
            lol = [val['init_frames'] for key, val in _s.sps_gi.items()]
            lol = [x for sublist in lol for x in sublist]  # flattening
            lol.sort(reverse=False)
            _s.sps_gi_init_frames = lol

            '''
            flat_list = []
            for sublist in lol:
                for item in sublist:
                    flat_list.append(item)
                    
             for sublist in lol: for item in sublist: yield item
            '''

        if P.A_SRS:
            '''HAVE TO STAY SEPARATED BCS TIED TO LS INIT FRAMES AND LD. 
            SOME REDUNDANCY BCS EVERYTHING ELSE IS SAME BUT WHATEVER'''
            _s.srs_gi0 = _s.gen_srs_gi0()
            _s.srs_gi1 = _s.gen_srs_gi1()
            _s.srs_gi2 = _s.gen_srs_gi2()
            _s.srs_gi3 = _s.gen_srs_gi3()
            _s.srs_gi4 = _s.gen_srs_gi4()

            _s.srs_gi = {  # these numbers correspond to c!
                '0': _s.srs_gi0,
                '1': _s.srs_gi1,
                '2': _s.srs_gi2,
                '3': _s.srs_gi3,
                '4': _s.srs_gi4,
            }

            _s.extend_srs_init_frames(EXTEND_PARAM=50)

            _s.srs_gi_init_frames = [val['init_frames'] for key, val in _s.srs_gi.items()]
            # _s.srs_gi_init_frames = list(np.asarray(_s.srs_gi_init_frames).flatten())  # ONLY WORKS IF SAME LENS
            _s.srs_gi_init_frames = [y for x in _s.srs_gi_init_frames for y in x]
            _s.srs_gi_init_frames.sort()

            aa = 5

        # if P.A_RS:
        #     # rs_init_frames = random.sample(range(min(pulse), max(pulse)), min(50, len(pulse)))
        #     # rs_init_frames = random.sample((START_F, P.FRAMES_STOP - 250), P.NUM_RS_2)
        #     rs_init_frames = random.sample(range(START_F, EXPL_F + 100), 50)
        #     # rs_init_frames = random.sample(range(0, 250), 180)
        #     rs_init_frames.sort(reverse=False)
        #     _s.rs_gi = _s.gen_rs_gi(rs_init_frames)

    def gen_ls_gi(_s, START_F, EXPL_F):

        """
        SHARED FOR THE SAME SH. Kind of... makes sense. ld is used for extent, but they are modified
        for each l in l class finish info.
        """

        lif0 = [START_F + 11]  # MUST START AT + 10
        lif1 = [START_F + 50]
        lif2 = [START_F + 100]
        lif3 = [START_F + 60]
        lif4 = [START_F + 150]
        l_init_frames = lif0 + lif1 + lif2 + lif3 + lif4

        l_gi = {
            'init_frames_all': l_init_frames,
            'lif0': lif0,
            'lif1': lif1,
            'lif2': lif2,
            'lif3': lif3,
            'lif4': lif4,
            'frames_tot0': EXPL_F - 100,  # THESE ARE GONA BECOME REALLY LONG
            'frames_tot1': P.FRAMES_STOP - lif1[-1],
            'frames_tot2': P.FRAMES_STOP - lif2[-1],
            'frames_tot3': P.FRAMES_STOP - lif3[-1],
            'frames_tot4': P.FRAMES_STOP - lif4[-1],
            'ld': _s.ld,  # USED BY SR?
            'ld0': [_s.ld[0] - 11, _s.ld[1] + 23],
            'ld1': [_s.ld[0] - 27, _s.ld[1] + 45],
            'ld2': [_s.ld[0] - 65, _s.ld[1] + 72],
            'ld3': [_s.ld[0] - 20, _s.ld[1] + 52],
            'ld4': [_s.ld[0] - 95, _s.ld[1] + 110],
            'scale': 0.5,
            'frame_ss': _s.frame_ss,
            'zorder': _s.zorder  # 3 is 110
        }

        return l_gi

    def extend_sps_init_frames(_s, EXTEND_PARAM):

        for key, val in _s.sps_gi.items():
            init_frames_out = val['init_frames']
            for i in range(1, EXTEND_PARAM):
                frames_tot = val['frames_tot']
                init_frame_new = val['init_frames'][-1] + frames_tot + 10
                # init_frames1 = [x + (i * (frames_tot + 10)) for x in val['init_frames']]

                # if init_frames1[-1] + frames_tot < P.FRAMES_STOP * 0.95:
                if init_frame_new + frames_tot + val['init_frame_max_dist'] < P.FRAMES_STOP * 0.95:
                    # init_frames_out.extend(init_frames1)
                    init_frames_out.append(init_frame_new)
                else:
                    pass
                    # print("2 sps init_frames1[-1] + frames_tot > P.FRAMES_STOP * 0.9")
                adf = 6

            val['init_frames'] = init_frames_out

    def extend_srs_init_frames(_s, EXTEND_PARAM):

        def add_more(init_frame_start, frames_tot):
            init_frames = []
            for init_frame in range(init_frame_start + 2 + frames_tot, init_frame_start + 20 + frames_tot, 3):
                if init_frame + frames_tot < P.FRAMES_STOP * 0.95:
                    init_frames.append(init_frame)
            return init_frames

        '''First just add more to the single first one'''
        for key, val in _s.srs_gi.items():
            val['init_frames'] = add_more(val['init_frames'][0], val['frames_tot'])

        for key, val in _s.srs_gi.items():
            if key == '0':
                continue
            # init_frames_out = val['init_frames']
            for i in range(1, EXTEND_PARAM):
                init_frame_last = val['init_frames'][-1]
                init_frames_new = add_more(init_frame_last, val['frames_tot'])
                val['init_frames'].extend(init_frames_new)

            adf =5

        adf = 5

    def gen_sps_gi0(_s, frames_tot):

        """
        MATCHED WITH ls gi, BUT THEYRE NOT CHILDREN AS FOR F -> SP (bcs problem there is that when F dies, then
        so does sp, so f has to last longer than sp).
        top left one
        THESE ARE AVERAGES
        r_f_s gives ratio of frames that should be discarded, i.e. the ratio that the sp should
        climb up the projectile (before shifting)

        OBS init_frame is set as random.randint(0, 100) in dyn_gen() SHOULD BE MOVED HERE.

        """

        sps_gi = {
            'gi_id': '0',
            'init_frames': copy.deepcopy(_s.ls_gi['lif0']),
            'frames_tot': frames_tot,  # NEEDS TO MATCH WITH EXPL ???
            'init_frame_max_dist': frames_tot - 50,  # OBS THIS MUST BE SHORTER
            'v_loc': 80, 'v_scale': 12,
            # 'num_loc': P.NUM_SPS_L, 'num_scale': P.NUM_SPS_L / 2,
            'theta_loc': -1.1, 'theta_scale': 0.05,  # neg is left  with straight down= -1.6, 0=
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.02,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 5, 'sp_len_scale': 5,
            'rgb_start': [0.4, 0.6],  #
            'rgb_theta_diff_c': 1,
            'rgb_v_diff_c': 0.01,
            'ld': [_s.ld[0] + 3, _s.ld[1] - 6],  # NOT TIED TO L BCS TUNING NEEDED ANYWAY
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [0, 0.01],
            'R_ss': [0.9, 1], 'R_scale': 0.2,
            'G_ss': [0.5, 0.2], 'G_scale': 0.15,
            'B_ss': [0.2, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'alpha_y_range': [0.01, 0.02],
            'up_down': 'down'
        }

        return sps_gi

    def gen_srs_gi0(_s):
        """ARE PICS SELECTED RANDOMLY"""

        '''WRONG. use extend_init_frames instead'''
        # init_frames = []
        # for i in range(-10, 10, 2):  # 5 total for each ls
        #     init_frame = _s.ls_gi['lif0'][0] + i
        #     init_frames.append(init_frame)

        srs_gi = {
            # 'l_id': 0,  # a position in a list
            'init_frames': [_s.ls_gi['lif0'][0]],
            'ld': _s.ls_gi['ld0'],
            'ld_offset_loc': [0, 0],  # THIS IS WRT ld0!
            'ld_offset_scale': [1, 3],  # OBS there is no ss, only start!
            'frames_tot': 200,
            'v_loc': 10,  # rc=2
            'v_scale': 2,
            'scale_ss': [0.01, 3],
            'theta_loc': -0.9,
            'theta_scale': 0, # 0.6 * 2 * np.pi,  # 2pi and pi are both straight up
            'rad_rot_loc': -1,
            'rad_rot_scale': 1,
            'r_f_d_loc': 0.05,
            'r_f_d_scale': 0.00,
            'up_down': 'up',
            'alpha_y_range': [0.01, 0.2],
            'zorder': _s.zorder + 10
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_sps_gi1(_s, frames_tot):

        """
        lower left one
        THESE ARE AVERAGES
        r_f_s gives ratio of frames that should be discarded, i.e. the ratio that the sp should
        climb up the projectile (before shifting)
        """


        sps_gi = {
            'gi_id': '1',
            'init_frames': copy.deepcopy(_s.ls_gi['lif1']),
            'frames_tot': frames_tot,
            'init_frame_max_dist': frames_tot - 50,  # random num of frames in future from init frame
            'v_loc': 100, 'v_scale': 10,
            # 'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
            'theta_loc': -0.9, 'theta_scale': 0.03,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'rgb_start': [0.4, 0.45],  #
            'rgb_theta_diff_c': 1,
            'rgb_v_diff_c': 0.01,
            'sp_len_loc': 5, 'sp_len_scale': 15,
            'ld': [_s.ld[0] - 4, _s.ld[1] + 15],
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [0, 0.1],
            'R_ss': [0.8, 1], 'R_scale': 0.2,
            'G_ss': [0.4, 0.2], 'G_scale': 0.2,
            'B_ss': [0.1, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'alpha_y_range': [0.05, 0.5],
            'up_down': 'down'
        }

        # 160, 77, 36  -> 76, 42, 28

        return sps_gi

    def gen_srs_gi1(_s):

        # in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi0, init_frames=init_frames_sr0)

        # assert (in_f[-1] < P.FRAMES_STOP)

        # init_frames = []
        # for i in range(-10, 10, 2):  # 5 total for each ls
        #     init_frame = _s.ls_gi['lif1'][0] + i
        #     init_frames.append(init_frame)

        srs_gi = {
            # 'l_id': 1,  # a position in a list
            'init_frames': [_s.ls_gi['lif1'][0]],
            'ld': _s.ls_gi['ld1'],
            'ld_offset_loc': [0, 0],  # OBS there is no ss, only start!
            'ld_offset_scale': [1, 3],  # OBS there is no ss, only start!
            'frames_tot': 200,
            'v_loc': 10,  # rc=2
            'v_scale': 2,
            'scale_ss': [0.01, 4],
            'theta_loc': -0.9,
            'theta_scale': 0.0, # 0.6 * 2 * np.pi,  # 2pi and pi are both straight up
            'rad_rot_loc': -1,
            'rad_rot_scale': 1,
            'r_f_d_loc': 0.05,
            'r_f_d_scale': 0.00,
            'up_down': 'up',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.zorder + 10
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_sps_gi2(_s, frames_tot):

        """
        lower left one
        THESE ARE AVERAGES
        r_f_s gives ratio of frames that should be discarded, i.e. the ratio that the sp should
        climb up the projectile (before shifting)
        """

        sps_gi = {
            'gi_id': '2',
            'init_frames': copy.deepcopy(_s.ls_gi['lif2']),
            'frames_tot': frames_tot,
            'init_frame_max_dist': frames_tot - 50,  # random num of frames in future from init frame
            'v_loc': 100, 'v_scale': 10,
            'theta_loc': -0.7, 'theta_scale': 0.03,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'rgb_start': [0.4, 0.45],  #
            'rgb_theta_diff_c': 1,
            'rgb_v_diff_c': 0.01,
            'sp_len_loc': 5, 'sp_len_scale': 15,
            'ld': [_s.ld[0] - 25, _s.ld[1] + 45],
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [0, 0.1],
            'R_ss': [0.8, 1], 'R_scale': 0.2,
            'G_ss': [0.4, 0.2], 'G_scale': 0.2,
            'B_ss': [0.1, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'alpha_y_range': [0.05, 0.5],
            'up_down': 'down'
        }

        # 160, 77, 36  -> 76, 42, 28

        return sps_gi

    def gen_srs_gi2(_s):

        # in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi0, init_frames=init_frames_sr0)

        # assert (in_f[-1] < P.FRAMES_STOP)

        # init_frames = []
        # for i in range(-10, 10, 2):  # 5 total for each ls
        #     init_frame = _s.ls_gi['lif2'][0] + i
        #     init_frames.append(init_frame)

        srs_gi = {
            # 'l_id': 2,  # a position in a list
            'init_frames': [_s.ls_gi['lif2'][0]],
            'ld': _s.ls_gi['ld2'],
            'ld_offset_loc': [0, 0],  # OBS there is no ss, only start!
            'ld_offset_scale': [1, 3],  # OBS there is no ss, only start!
            'frames_tot': 200,
            'v_loc': 10,  # rc=2
            'v_scale': 2,
            'scale_ss': [0.01, 3],
            'theta_loc': -0.9,  # 0.6 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.0,
            'rad_rot_loc': -1,
            'rad_rot_scale': 1,
            'r_f_d_loc': 0.05,
            'r_f_d_scale': 0.00,
            'up_down': 'up',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.zorder + 10
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_sps_gi3(_s, frames_tot):

        """
        lower left one
        THESE ARE AVERAGES
        r_f_s gives ratio of frames that should be discarded, i.e. the ratio that the sp should
        climb up the projectile (before shifting)
        """

        sps_gi = {
            'gi_id': '3',
            'init_frames': copy.deepcopy(_s.ls_gi['lif3']),
            'frames_tot': frames_tot,
            'init_frame_max_dist': frames_tot - 50,  # random num of frames in future from init frame
            'v_loc': 100, 'v_scale': 10,
            # 'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
            'theta_loc': -1.1, 'theta_scale': 0.1,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'rgb_start': [0.4, 0.45],  #
            'rgb_theta_diff_c': 1,
            'rgb_v_diff_c': 0.01,
            'sp_len_loc': 5, 'sp_len_scale': 15,
            'ld': [_s.ld[0] - 0, _s.ld[1] + 17],
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [0.1, 0.1],
            'R_ss': [0.8, 1], 'R_scale': 0.2,
            'G_ss': [0.4, 0.2], 'G_scale': 0.2,
            'B_ss': [0.1, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'alpha_y_range': [0.01, 0.9],
            'up_down': 'down'
        }

        # 160, 77, 36  -> 76, 42, 28

        return sps_gi

    def gen_srs_gi3(_s):

        # in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi0, init_frames=init_frames_sr0)

        # assert (in_f[-1] < P.FRAMES_STOP)

        # init_frames = []
        # for i in range(-10, 10, 2):  # 5 total for each ls
        #     init_frame = _s.ls_gi['lif3'][0] + i
        #     init_frames.append(init_frame)

        srs_gi = {
            # 'l_id': 3,  # a position in a list
            'init_frames': [_s.ls_gi['lif3'][0]],
            'ld': _s.ls_gi['ld3'],
            'ld_offset_loc': [0, 0],  # OBS there is no ss, only start!
            'ld_offset_scale': [1, 3],  # OBS there is no ss, only start!
            'frames_tot': 200,
            'v_loc': 10,  # rc=2
            'v_scale': 2,
            'scale_ss': [0.01, 4],
            'theta_loc': -0.9,  # 0.6 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.0,
            'rad_rot_loc': -1,
            'rad_rot_scale': 1,
            'r_f_d_loc': 0.05,
            'r_f_d_scale': 0.00,
            'up_down': 'up',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.zorder + 10
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_sps_gi4(_s, frames_tot):

        """
        lower left one
        THESE ARE AVERAGES
        r_f_s gives ratio of frames that should be discarded, i.e. the ratio that the sp should
        climb up the projectile (before shifting)
        """

        sps_gi = {
            'gi_id': '4',
            'init_frames': copy.deepcopy(_s.ls_gi['lif4']),
            'frames_tot': frames_tot,
            'init_frame_max_dist': frames_tot - 50,  # random num of frames in future from init frame
            'v_loc': 100, 'v_scale': 10,
            'theta_loc': -0.7, 'theta_scale': 0.03,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'rgb_start': [0.4, 0.45],  #
            'rgb_theta_diff_c': 1,
            'rgb_v_diff_c': 0.01,
            'sp_len_loc': 5, 'sp_len_scale': 15,
            'ld': [_s.ld[0] - 50, _s.ld[1] + 75],
            'ld_offset_loc': [0, 0],
            'ld_offset_scale': [0, 0.1],
            'R_ss': [0.8, 1], 'R_scale': 0.2,
            'G_ss': [0.4, 0.2], 'G_scale': 0.2,
            'B_ss': [0.1, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'alpha_y_range': [0.05, 0.5],
            'up_down': 'down'
        }

        # 160, 77, 36  -> 76, 42, 28

        return sps_gi

    def gen_srs_gi4(_s):

        # in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi0, init_frames=init_frames_sr0)

        # assert (in_f[-1] < P.FRAMES_STOP)

        # init_frames = []
        # for i in range(-10, 10, 2):  # 5 total for each ls
        #     init_frame = _s.ls_gi['lif4'][0] + i
        #     init_frames.append(init_frame)

        srs_gi = {
            # 'l_id': 3,  # a position in a list
            'init_frames': [_s.ls_gi['lif4'][0]],
            'ld': _s.ls_gi['ld4'],
            'ld_offset_loc': [0, 0],  # OBS there is no ss, only start!
            'ld_offset_scale': [1, 3],  # OBS there is no ss, only start!
            'frames_tot': 200,
            'v_loc': 10,  # rc=2
            'v_scale': 2,
            'scale_ss': [0.01, 4],
            'theta_loc': -0.9,  # 0.6 * 2 * np.pi,  # 2pi and pi are both straight up
            'theta_scale': 0.0,
            'rad_rot_loc': -1,
            'rad_rot_scale': 1,
            'r_f_d_loc': 0.05,
            'r_f_d_scale': 0.00,
            'up_down': 'up',
            'alpha_y_range': [0, 0.2],
            'zorder': _s.zorder + 10
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_rs_gi(_s, rs_init_frames, _type=None):
        rs_gi = {}

        rs_gi['init_frames'] = rs_init_frames
        rs_gi['init_frames'].sort()

        # rs_gi['init_frames'] = list(range(3, 63))  # TODO: This should be generated same frame
        rs_gi['frames_tot'] = 200
        # rs_gi['frames_tot'] = 300

        assert (rs_gi['init_frames'][-1] + rs_gi['frames_tot'] < P.FRAMES_STOP)
        rs_gi['ld'] = [_s.ld[0] - 0, _s.ld[1] - 0]  # -6 TUNED WITH affine2D.translate!!!
        rs_gi['ld_offset_loc'] = [0, 0]  # OBS there is no ss, only start!
        rs_gi['ld_offset_scale'] = [4, 10]  # OBS there is no ss, only start!
        rs_gi['frame_ss'] = _s.frame_ss  # simpler with this
        rs_gi['rs_hardcoded'] = {}
        rs_gi['v_loc'] = 100  # rc=2
        rs_gi['v_scale'] = 20
        rs_gi['theta_loc'] = -1.0  # radians!
        rs_gi['theta_scale'] = 0.1
        rs_gi['r_f_d_loc'] = 0.1
        rs_gi['r_f_d_scale'] = 0.02
        rs_gi['scale_loc'] = 0.2
        rs_gi['scale_scale'] = 0.1
        rs_gi['up_down'] = 'down'
        # rs_gi['alpha_plot'] = 'r_down'
        rs_gi['zorder'] = 300

        return rs_gi
