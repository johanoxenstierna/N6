import copy
import random
import numpy as np


def simple_projectile(gi=None):
    """
    OBS this is for midpoint, i.e. SINGLE PIXEL
    See tutorial for using a patch to make it larger than single pixel
    always assumes origin is at 0, 0, so needs shifting afterwards.
    ALSO, THIS FUNCTION ALWAYS OUTPUTS RIGHT MOTION, UNTIL IT IS SET BELOW
    """

    '''HERE TUNE THETA BASED ON V. THETA CLOSE TO 0 -> MORE V'''

    xy = np.zeros((gi['frames_tot'], 2))  # MIDPOINT

    G = 9.8

    # t_flight = 6 * v * np.sin(theta) / G
    t_flight = 5 * gi['v'] * np.sin(gi['theta']) / G  # 4 means they land at origin. 5 little bit below
    t = np.linspace(0, t_flight, gi['frames_tot'])
    t_lin = np.linspace(0, t_flight, gi['frames_tot'])
    # t_geo = np.geomspace(0.08, t_flight ** 1.2, gi['frames_tot'])
    t_geo_0 = np.geomspace(0.5, t_flight ** 1, gi['frames_tot'])  # POWER CONTROLS DISTANCE
    t_geo_1 = np.geomspace(0.5, t_flight ** 1, gi['frames_tot'])

    x = gi['v'] * np.cos(gi['theta']) * t
    x_lin = abs(gi['v'] * np.cos(gi['theta']) * t_lin)  # THIS IS ALWAYS POSITIVE
    x_geo = abs(2 * gi['v'] * np.cos(gi['theta']) * t_geo_0)  # THIS IS ALWAYS POSITIVE. KEEP IT SIMPLE
    # x = 0.0001 * x_lin * t_lin + 0.2 * x_lin * x_geo
    # x = 0.00001 * x_lin * t_lin + 0.1 * x_lin * x_geo
    # x = 0.001 * x_lin * t_lin + 0.005 * x_lin * x_geo
    # x = 0.05 * x_lin + 0.95 * x_geo
    x = x_geo

    '''If theta is close enough '''

    adf = - 0.5 * G * t_lin ** 2
    gg = np.sin(gi['theta'])
    y_lin = gi['v'] * np.sin(gi['theta']) * 2 * t_lin #- 0.5 * G * t_lin ** 2  # OBS OBS this affect both up and down equally
    y_geo = gi['v'] * np.sin(gi['theta']) * 2 * t_geo_1 - 0.5 * G * t_geo_1 ** 2

    # y = 0.3 * y_lin + 0.7 * y_geo  # THIS AFFECTS HOW FAR DOWN THEY GO
    # y = 0.05 * y_lin + 0.95 * y_geo  # THIS AFFECTS HOW FAR DOWN THEY GO
    y = y_geo  # THIS AFFECTS HOW FAR DOWN THEY GO

    xy[:, 0] = x
    xy[:, 1] = y

    return xy

def flip_projectile_x(sp):
    """Only works for sp"""

    # PEND DEL 
    if sp.gi['ld_init'][0] < sp.f.gi['left_mid']:  # flip x values
        sp.xy_t[:, 0] = -sp.xy_t[:, 0]

    # let a random subset still go over middle
    dist_to_mid = abs(sp.gi['ld'][0] - 640)
    if dist_to_mid < 50 and sp.gi['dist_to_theta_0'] < 0.4:
        if random.random() < 0.4:
            if sp.gi['ld'][0] < sp.f.gi['left_mid']:
                sp.xy_t[:, 0] = -sp.xy_t[:, 0]
    elif dist_to_mid < 100 and sp.gi['dist_to_theta_0'] < 0.2:
        if random.random() < 0.2:
            if sp.gi['ld'][0] < sp.f.gi['left_mid']:
                sp.xy_t[:, 0] = -sp.xy_t[:, 0]


    return sp.xy_t

# def shift_projectile(xy_t, origin=None, frames_tot_d=None, up_down=None, r_f_d_type=''):
def shift_projectile(xy_t, origin=None, gi=None):
    """
    OBS N6 = its hardcoded for sp
    shifts it to desired xy
    y is flipped because 0 y is at top and if flip_it=True
    """

    xy = copy.deepcopy(xy_t)

    '''THIS MAKES THEM NEVER CROSS MIDDLE'''
    if origin[0] < 640 and xy[0, 0] < xy[-1, 0]:  # TO THE LEFT BUT POSITIVE
        xy[:, 0] = -xy[:, 0]
    elif origin[0] > 640 and xy[0, 0] > xy[-1, 0]:  # TO THE RIGHT BUT NEGATIVE
        xy[:, 0] = -xy[:, 0]

    # '''let a random subset still go over middle'''
    dist_to_mid = abs(origin[0] - 640)
    if dist_to_mid < 50 and gi['dist_to_theta_0'] < 0.4:
        if random.random() < 0.4:
            if origin[0] < 640:
                xy[:, 0] = -xy[:, 0]
    elif dist_to_mid < 100 and gi['dist_to_theta_0'] < 0.2:
        if random.random() < 0.2:
            if origin[0] < 640:
                xy[:, 0] = -xy[:, 0]

    # if gi['out_screen']:
    #     xy = xy[:int(len(xy) / 2), :int(len(xy) / 2)]
    #     gi['frames_tot'] = len(xy)

    if gi['up_down'] == 'up' or gi['up_down'] == 'down':
        xy[:, 1] *= -1  # flip it. Now all neg


    '''x'''
    xy[:, 0] += origin[0]  # OBS THIS ORIGIN MAY BE BOTH LEFT AND RIGHT OF 640

    '''
    y1: Move. y_shift_r_f_d is MORE shifting downward (i.e. positive), but only the latter portion 
    of frames is shown.
    '''
    xy[:, 1] += origin[1] - xy[0, 1]



    return xy

