

from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np
import copy

class Sh_4_info(ShInfoAbstract):

    """

    """

    def __init__(_s, START_F, EXPL_F, top_point):
        super().__init__()
        _s.id = '4'
        _s.extent = "static"
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        _s.frames_tot = _s.frame_ss[1] - _s.frame_ss[0]  # l frames_tot set below

        _s.ld = top_point
        _s.child_names = ['sps', 'ls', 'rs', 'srs']

        _s.zorder = 130

        # l_init_frames = [130, 220, 250, 300]
        # l_init_frames = [10, 50, 200, 300]
        # l_init_frames = [10, 30, 60, 300]
        _s.ls_gi = _s.gen_ls_gi(START_F, EXPL_F)

        _s.num_sp_at_init_frame = 50  # OBS this is a special parameter.

        if P.A_SPS:
            # init_frames_sp0 = [pulse[0] - 100, pulse[0], pulse[1] + 100]
            # init_frames_sp1 = [pulse[1] - 100, pulse[1], pulse[1] + 100]  # 150 is init_frame_max_dist
            # init_frames_sp2 = [pulse[2] - 100, pulse[2], pulse[2] + 100]  # 150 is init_frame_max_dist
            # init_frames_sp3 = [pulse[3] - 100, pulse[3], pulse[3] + 100]  # 150 is init_frame_max_dist

            _s.sps_gi0 = _s.gen_sps_gi0(frames_tot=350)
            _s.sps_gi1 = _s.gen_sps_gi1(frames_tot=350)
            # _s.sps_gi2 = _s.gen_sps_gi2(init_frames_sp2)
            # _s.sps_gi3 = _s.gen_sps_gi3(init_frames_sp3)

            _s.sps_gi = {
                '0': _s.sps_gi0,
                '1': _s.sps_gi1
                # '2': _s.sps_gi2,
                # '3': _s.sps_gi3
            }

            _s.extend_sps_init_frames(EXTEND_PARAM=50)

            lol = [val['init_frames'] for key, val in _s.sps_gi.items()]
            lol = [x for sublist in lol for x in sublist]
            lol.sort(reverse=False)
            _s.sps_gi_init_frames = lol

        if P.A_SRS:

            _s.srs_gi0 = _s.gen_srs_gi0()
            _s.srs_gi1 = _s.gen_srs_gi1()


            _s.srs_gi = {  # these numbers correspond to c!
                '0': _s.srs_gi0,
                '1': _s.srs_gi1  # IF A C AND CORR SR EXISTS, THEN SO MUST THIS
                # '2': _s.srs_gi2,
                # '3': _s.srs_gi3,
                # '4': _s.srs_gi4,
                # '5': _s.srs_gi5,
                # '6': _s.srs_gi6
            }

            _s.srs_gi_init_frames = [val['init_frames'] for key, val in _s.srs_gi.items()]
            _s.srs_gi_init_frames = list(np.asarray(_s.srs_gi_init_frames).flatten())

        if P.A_RS:
            rs_init_frames = random.sample(range(1, 300), 50)
            _s.rs_gi = _s.gen_rs_gi(rs_init_frames)

    def gen_ls_gi(_s, START_F, EXPL_F):

        """
        SHARED FOR THE SAME SH. Kind of... makes sense. ld is used for extent, but they are modified
        for each l in l class finish info.
        """

        # lif0, lif1 = _s.distribute_pulse_for_ls(pulse)  # l_init_frame
        lif0 = [START_F + 100]
        lif1 = [START_F + 150]
        # lif2 = [pulse[2]]
        # lif3 = [pulse[3]]
        l_init_frames = lif0 + lif1 #+ lif2 + lif3

        l_gi = {
            'init_frames_all': l_init_frames,
            'lif0': lif0,
            'lif1': lif1,
            # 'lif2': lif2,
            # 'lif3': lif3,
            'frames_tot0': P.FRAMES_STOP - lif0[-1],
            'frames_tot1': P.FRAMES_STOP - lif1[-1],
            # 'frames_tot2': 500,
            # 'frames_tot3': 500,
            'ld': _s.ld,  # USED BY SR?
            'ld0': [_s.ld[0] + 4, _s.ld[1] + 30],
            'ld1': [_s.ld[0] + 19, _s.ld[1] + 70],
            # 'ld2': [_s.ld[0] - 65, _s.ld[1] + 72],
            # 'ld3': [_s.ld[0] - 20, _s.ld[1] + 52],
            'frame_ss': _s.frame_ss,
            'scale': 0.5,
            'zorder': 120  # 3 is 110
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
            'frames_tot': frames_tot,  # NEEDS TO MATCH WITH EXPL
            'init_frame_max_dist': 100,  # OBS THIS MUST BE SHORTER
            'v_loc': 80, 'v_scale': 12,
            # 'num_loc': P.NUM_SPS_L, 'num_scale': P.NUM_SPS_L / 2,
            'theta_loc': 0.9, 'theta_scale': 0.01,  # neg is left  with straight down= -1.6, 0=
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.02,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'sp_len_loc': 5, 'sp_len_scale': 5,
            'rgb_start': [0.4, 0.5],  #
            'rgb_theta_diff_c': 1,
            'rgb_v_diff_c': 0.01,
            'ld': [_s.ld[0] + 3, _s.ld[1] + 10],
            'ld_offset_loc': [0, 0.1],
            'ld_offset_scale': [3, 1],
            'R_ss': [0.9, 1], 'R_scale': 0.2,
            'G_ss': [0.5, 0.2], 'G_scale': 0.15,
            'B_ss': [0.2, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'alpha_y_range': [0.01, 0.6],
            'up_down': 'down'
        }

        return sps_gi

    def gen_srs_gi0(_s):
        """ARE PICS SELECTED RANDOMLY"""
        # in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi0, init_frames=init_frames_sr0)

        init_frames = []
        for i in range(-10, 10, 3):  # 5 total for each ls
            init_frame = _s.ls_gi['lif0'][0] + i
            init_frames.append(init_frame)

        srs_gi = {
            # 'l_id': 0,  # a position in a list
            'init_frames': init_frames,
            'ld': _s.ls_gi['ld0'],
            'ld_offset_loc': [-5, 5],  # OBS there is no ss, only start!
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
            'alpha_y_range': [0.01, 0.2],
            'zorder': _s.zorder + 10
        }

        assert (srs_gi['init_frames'][-1] + srs_gi['frames_tot'] < P.FRAMES_STOP)

        return srs_gi

    def gen_sps_gi1(_s, frames_tot):

        """
        """

        sps_gi = {
            'gi_id': '1',
            'init_frames': copy.deepcopy(_s.ls_gi['lif1']),
            'frames_tot': frames_tot,
            'init_frame_max_dist': 100,  # random num of frames in future from init frame
            'v_loc': 100, 'v_scale': 10,
            # 'num_loc': P.NUM_SPS_F, 'num_scale': P.NUM_SPS_F / 2,
            'theta_loc': 1.0, 'theta_scale': 0.05,
            'r_f_d_loc': 0.1, 'r_f_d_scale': 0.05,
            'r_f_d_type': 'after',  # which part of r_f_d to use
            'rgb_start': [0.4, 0.45],  #
            'rgb_theta_diff_c': 1,
            'rgb_v_diff_c': 0.01,
            'sp_len_loc': 5, 'sp_len_scale': 15,
            'ld': [_s.ld[0] + 23, _s.ld[1] + 23],
            'ld_offset_loc': [-4, 5],
            'ld_offset_scale': [0, 0.1],
            'R_ss': [0.8, 1], 'R_scale': 0.2,
            'G_ss': [0.4, 0.2], 'G_scale': 0.2,
            'B_ss': [0.1, 0.05], 'B_scale': 0.01,  # good to prevent neg numbers here
            'alpha_y_range': [0.05, 0.9],
            'up_down': 'down'
        }

        return sps_gi

    def gen_srs_gi1(_s):
        """ARE PICS SELECTED RANDOMLY"""
        # in_f, init_frames, frames_tot = _s.gen_srs_init_frames(_cs_gi=_s.cs_gi0, init_frames=init_frames_sr0)

        init_frames = []
        for i in range(-10, 10, 3):  # 5 total for each ls
            init_frame = _s.ls_gi['lif1'][0] + i
            init_frames.append(init_frame)

        srs_gi = {
            # 'l_id': 0,  # a position in a list
            'init_frames': init_frames,
            'ld': _s.ls_gi['ld1'],
            'ld_offset_loc': [-5, 5],  # OBS there is no ss, only start!
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
            'alpha_y_range': [0.01, 0.2],
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
        rs_gi['ld_offset_loc'] = [-1, 2]  # OBS there is no ss, only start!
        rs_gi['ld_offset_scale'] = [0.2, 0.05]  # OBS there is no ss, only start!
        rs_gi['frame_ss'] = _s.frame_ss  # simpler with this
        rs_gi['rs_hardcoded'] = {}
        rs_gi['v_loc'] = 12  # rc=2
        rs_gi['v_scale'] = 10
        rs_gi['theta_loc'] = np.pi/2 + 0.3  # radians!
        rs_gi['theta_scale'] = 0.02
        rs_gi['r_f_d_loc'] = 0.01
        rs_gi['r_f_d_scale'] = 0.02
        rs_gi['scale_loc'] = 0.15
        rs_gi['scale_scale'] = 0.05
        rs_gi['up_down'] = 'down'
        rs_gi['alpha_plot'] = 'r_down'
        rs_gi['zorder'] = 300

        return rs_gi
