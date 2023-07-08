import copy
import random
import numpy as np


def simple_projectile(v, theta, frames_tot, rc=1, up_down=None):
    """
    OBS this is for midpoint, i.e. SINGLE PIXEL
    See tutorial for using a patch to make it larger than single pixel
    always assumes origin is at 0, 0, so needs shifting afterwards.
    """

    '''HERE TUNE THETA BASED ON V. THETA CLOSE TO 0 -> MORE V'''

    xy = np.zeros((frames_tot, 2))  # MIDPOINT

    G = 9.8
    # t_flight = 2 * v * np.sin(theta) / G
    # t = np.linspace(0, t_flight, num_frames)
    # x = v * np.cos(theta) * t
    # y = v * np.sin(theta) * t - 0.5 * G * t ** 2

    # t_flight = 6 * v * np.sin(theta) / G
    t_flight = 5 * v * np.sin(theta) / G  # 4 means they land at origin. 5 little bit below
    t = np.linspace(0, t_flight, frames_tot)

    # TEST W DIFF FUNCS ===================
    # if up_down == 'down':
    #     t_flight = 0.05 * v * np.sin(theta) / G
    #     t = np.linspace(0, t_flight, frames_tot)
    # ======================================
    # v = np.linspace(v * 1.1, v * 0.3, num=len(t))
    # x = v * np.cos(theta) * t
    x = v * np.cos(theta) * t ** 1.5
    # y = v * np.sin(theta) * 2 * t - 0.5 * G * t ** 2
    y = v * np.sin(theta) * 2 * t - 0.5 * G * t ** 2  # OBS OBS this affect both up and down equally

    '''y max is always in middle. so manually set v0 to lower than v1'''
    # x0 = v * np.cos(theta) * t
    # x1 = 2 * v * np.cos(theta) * t
    #
    # y0 = v * np.sin(theta) * t - 0.5 * G * t ** 2
    # y1 = v * np.sin(theta) * t - 0.5 * G * t ** 2.2


    # geomx0 = np.geomspace(0.001, 1, int(len(y) / 2))
    # geomx1 = np.geomspace(1, 200, int(len(y) / 2))
    # geomy0 = np.linspace(0, 1, int(len(y) / 2))
    # geomy1 = -np.linspace(0.001, 20, int(len(y) / 2))

    # if theta < 0.5 * np.pi:
    #     x[:100] = x[:100] + geomx0
    #     x[100:] = x[100:] + geomx1
    # else:
    #     raise Exception("Asdf")
        # x[:100] = x[:100] + geomx0
        # x[100:] = x[100:] + geomx1

    # A = y[:100] * geomy0
    # B = y[100:] * geomy1

    dff = 5

    # TEST W DIFF FUNCS ===================
    '''Linear'''
    # x = -v * t  * 0.2 * np.sin(theta)
    # y = -v * t  * 0.3 * np.cos(theta)

    # if up_down == 'down':
    #     x = v * np.cos(theta) * t
    #     y = -v * np.sin(theta - 0.5) * rc * t - 0.5 * G * t ** 2

    # x = v * np.sin(theta) * t
    # y = v * np.cos(theta) * rc * t - 0.5 * G * t ** 2
    # =====================================


    xy[:, 0] = x
    xy[:, 1] = y


    return xy


# def shift_projectile(xy_t, origin=None, frames_tot_d=None, up_down=None, r_f_d_type=''):
def shift_projectile(xy_t, origin=None, frames_tot_d=None, gi=None):
    """
    OBS N6 = its hardcoded for sp
    shifts it to desired xy
    y is flipped because 0 y is at top and if flip_it=True
    """

    xy = copy.deepcopy(xy_t)

    if gi['out_screen']:
        xy = xy[:int(len(xy) / 2), :int(len(xy) / 2)]
        gi['frames_tot'] = len(xy)

    '''
    y0: First it needs to be flipped bcs all values are pos to start with, but it needs to be neg.  
    '''
    # if up_down == 'up' or up_down == 'down':
    #     xy[:, 1] *= -1  # flip it. Now all neg

    if gi['up_down'] == 'up' or gi['up_down'] == 'down':
        xy[:, 1] *= -1  # flip it. Now all neg

    try:
        x_shift_r_f_d = xy[0, 0]  # TODO: change for left motion
        y_shift_r_f_d = xy[0, 1]
    except:
        raise Exception("adf")

    '''x'''
    xy[:, 0] += origin[0] - x_shift_r_f_d  # x

    '''
    y1: Move. y_shift_r_f_d is MORE shifting downward (i.e. positive), but only the latter portion 
    of frames is shown.
    '''
    xy[:, 1] += origin[1] - y_shift_r_f_d



    return xy


def falling_projectile(gi):
    """v is downward """
    G = 9.8
    t_flight = np.sqrt((2 * gi['height']) / G)
    t = np.linspace(0, t_flight, gi['frames_tot'])
    v_y = 0  # starts at 0

    xy = np.zeros((gi['frames_tot'], 2))

    y_ = np.linspace(0, gi['height'], gi['frames_tot'])
    xy[:, 1] = y_

    # '''y motion'''
    # for i in range(len(xy)):
    #     y_dist = (v_y * t[i]) - (0.5 * G * t[i]**2)
    #     xy[i, 1] = y_dist

    '''x motion'''

    # input = np.linspace(1, 30, num=len(xy))

    if gi['9_id'] == '0':  # pillar

        # left_right = np.random.choice(['left', 'right'], p=[0.4, 0.6])
        # left_right = 'left'
        # c = gi['c']
        # if left_right == 'left':
        #     c = -gi['c']
        # input = np.linspace(1, 3, num=len(xy))  # more=more speed
        # xy[:, 0] = c * np.exp(input**2)

        height = random.randint(gi['height'] - 50, gi['height'] + 50)
        y_ = np.linspace(0, height, gi['frames_tot'])
        xy[:, 1] = y_


        input = np.linspace(0, 4, num=len(xy))  # more=more speed
        aa = -5 * np.exp(input)
        # xy[:, 0] = np.linspace(0, -50, num=gi['frames_tot'])
        xy[:, 0] = aa

        ss = 6
    elif gi['9_id'] == '1':  # flat
        left_right = 'right'  # np.random.choice(['left', 'right'], p=[0.2, 0.8])
        left_right = np.random.choice(['left', 'right'], p=[0.5, 0.5])
        c = gi['c']
        if left_right == 'left':
            c = -gi['c']
        input = np.linspace(0, 4, num=len(xy))  # more=more speed
        aa = c * np.exp(input)
        xy[:, 0] = aa

        xy[:, 1] = -xy[:, 1]

        dfdf = 5

    return xy

