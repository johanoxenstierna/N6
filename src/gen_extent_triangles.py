import numpy as np
from copy import deepcopy
import math
# from src.trig_functions import _normal
import P


def gen_zig_zag(num_frames, cycles, max_delta_width):
    """Provided as a width delta ratio"""

    x = np.arange(start=0, stop=num_frames)

    cycles_currently = num_frames / (2 * np.pi)
    denominator = cycles_currently / cycles

    zigzag = np.sin(x / denominator) * max_delta_width / 2 + (1 - max_delta_width / 2)  # shrink then shift
    # the div / 2 is there bcs its both pos and neg (alternatively shift it to pos first for better understandability)
    # mi, ma = np.min(zigzag), np.max(zigzag)

    return zigzag


# def gen_extent(gi, pic, scale_vector=(), lds_vec=(), zigzag=()):
#
#     """
#     gi=general info. Standardized format
#     left right down up
#     returns linear motion extent through time
#     if linear motion not desired then provide above arguments.
#     extent_t is the same thing but shifted to origin at lt (since tri's have origin there).
#     extent_t == UNSHIFTED FRAME
#     height_m: modified with scale
#     OBS this only has capability to grow objects to the right, so left smokrs need modification to look good.
#     """
#
#     frame_num = gi['frame_ss'][1] - gi['frame_ss'][0]  # ALWAYS
#
#     extent = np.zeros((frame_num, 4))  # left, right, bottom, top borders
#     extent_t = np.zeros((frame_num, 4))  # left, right, bottom, top borders
#
#     '''Below may will be introduced if non-linear motion is needed. If so then provide it
#     as argument. Same with lds. '''
#     # if len(scale_vector) > 0:
#     #     scale_vector = scale_vector
#     # else:
#     #     assert(gi['scale_ss'] != "abstractSS")
#
#     scale_vector = np.linspace(gi['scale_ss'][0], gi['scale_ss'][1], frame_num)
#
#     # if len(lds_vec) > 0:
#     #     lds_vec = lds_vec
#     # else:
#     lds_vec = np.linspace(gi['ld_ss'][0], gi['ld_ss'][1], frame_num)  # left downs through time
#
#     width = pic.shape[1]
#     height = pic.shape[0]
#
#     for i in range(frame_num):
#         # if len(zigzag) < 1:  # perhaps reintroduced later
#         width_m = width * scale_vector[i]
#         # else:
#         #     width_m = width * scale_vector[i] * zigzag[i]
#
#         height_m = height * scale_vector[i]
#
#         extent[i] = [lds_vec[i, 0],  # left
#                      lds_vec[i, 0] + width_m,  # right
#                      # lds_vec[i, 1] + (1 - y_mid) * height_m,  # down
#                      lds_vec[i, 1] + 0,  # down
#                      # lds_vec[i, 1] - y_mid * height_m  # up
#                      lds_vec[i, 1] - height_m  # up
#                      ]
#
#         extent_t[i] = [extent[i, 0] - extent[0, 0],  # left
#                        extent[i, 1] - extent[0, 0],  # right
#                        extent[i, 2] - extent[0, 3],  # down
#                        extent[i, 3] - extent[0, 3]]  # up
#
#     assert(np.isclose(a=extent_t[0, 0], b=0.0))
#     assert(np.isclose(a=extent_t[0, 3], b=0.0))
#
#     # WHEN y_mid IS LESS THAN 1.0, THE WHOLE THING NEEDS TO BE SHIFTED
#
#     # DEPR because only tris shifted.
#     # # UNSHIFT WHEN EXTENT FRAME IS LARGER THAN WHAT IS PERMITTED BY LDS_LOG
#     # diff_do = extent[0, 2] - lds_vec[0, 1]  # if the first tri wants to go further down than what lds_vec permits
#     # if diff_do > 0:  # This means y_mid is less than 1
#     #     # extent[:, 2] -= diff_do
#     #     # extent[:, 3] -= diff_do
#     #     extent_t[:, 2] -= diff_do
#     #     extent_t[:, 3] -= diff_do
#     #
#     # diff_le = extent[0, 0] - lds_vec[0, 0]  # if the first tri wants to go further  than what lds_vec permits
#     # if diff_le > 0:  # This means y_mid is less than 1
#     #     # extent[:, 2] -= diff_le
#     #     # extent[:, 3] -= diff_le
#     #     extent_t[:, 2] -= diff_le
#     #     extent_t[:, 3] -= diff_le
#
#     return extent, extent_t, lds_vec, scale_vector


def gen_triangles(extent_t, extent, gi, pic):
    """
    tri_max is needed for warpAffine. Since the warp is only on a subpic, tri_max gives the needed extent.
    padding returned, NOT shape after warpAffine obviously since this is not known at this stage
    tri_base not the same as tris (u f* idiot) A REFERENCE TO ORIG SCALE NEEDED.
    Mask is not part of warp!
    TODO: check whether this works for SPLLLLL
    """

    # 1 BUILD TRIANGLES in extent_t domain ==============================
    # ext = extent_t[0]
    width = pic.shape[1]
    height = pic.shape[0]

    tris = []

    # CORRESPONDS TO EXTENT_T[0]
    p0 = [0, height]
    p1 = [0 + (width / 2), 0]
    p2 = [0 + width, height]

    tri_base = np.float32([p0, p1, p2])

    tri_ext = {'min_le': 9999, 'min_le_i': None,
               'max_le': -9999, 'max_le_i': None,
               'max_ri': -9999, 'max_ri_i': None,
               'min_do': 9999, 'min_do_i': None,
               'max_do': -9999, 'max_do_i': None
               }
    # tri_min_le, tri_min_le_i = 9999, None
    # tri_max_le, tri_max_le_i = -9999, None
    # tri_max_ri, tri_max_ri_i = -9999, None
    # tri_min_do, tri_min_do_i = 9999, None
    # tri_max_do, tri_max_do_i = -9999, None

    for i in range(0, extent_t.shape[0]):

        ext = extent_t[i]

        width = ext[1] - ext[0]
        height = ext[2] - ext[3]

        p0 = [ext[0], ext[3] + height]
        p1 = [ext[0] + (width / 2), ext[3]]
        p2 = [ext[0] + width, ext[3] + height]

        tri = np.float32([p0, p1, p2])
        tris.append(tri)

        if p0[0] < tri_ext['min_le']:
            tri_ext['min_le'] = p0[0]
            tri_ext['min_le_i'] = i
        if p0[0] > tri_ext['max_le']:
            tri_ext['max_le'] = p0[0]
            tri_ext['max_le_i'] = i
        if p2[0] > tri_ext['max_ri']:
            tri_ext['max_ri'] = p2[0]
            tri_ext['max_ri_i'] = i
        if p1[1] < tri_ext['min_do']:
            tri_ext['min_do'] = p1[1]
            tri_ext['min_do_i'] = i
        if p0[1] > tri_ext['max_do']:
            tri_ext['max_do'] = p0[1]
            tri_ext['max_do_i'] = i

    # SHIFT TRIANGLES
    # tris_s = shift_triangles(deepcopy(tris), gi, extent_t, tri_ext)
    tris_s = shift_triangles_N4(deepcopy(tris), gi, extent_t, tri_ext)
    # tris_s =tris
    ## 3. BUILD MASK SHAPE: If ===================================

    if extent[-1, 1] > extent[0, 1]:  # MOVED TO RIGHT
        mask_ri = int(extent[-1, 1])
    elif extent[0, 1] > extent[-1, 1]:  # MOVED TO LEFT
        mask_ri = int(extent[0, 1])

    # mask_ri += gi['extra_offset_x']

    # if tri_ext['max_ri'] < extent[0, 1]:  # this means it has moved to right
    #     diff = tri_ext['max_ri']
    #     mask_ri = int(extent[0, 1] + diff)

    # if tri_ext['max_le'] < max(gi['ld_ss'][0][0], gi['ld_ss'][1][0]):  # ld_ss is a bit weird (first start/stop, then ld)
    #     diff = max(gi['ld_ss'][0][0], gi['ld_ss'][1][0]) - tri_ext['max_le']
    #     mask_ri = int(tris_s[tri_ext['max_ri_i']][2][0] + diff)  # the tri with the max le, then use third point and its x
    #     # mask_ri += extent[-1, 0]
    # elif tri_ext['max_le'] > max(gi['ld_ss'][0][0], gi['ld_ss'][1][0]):
    #     pass
    # else:
    #     mask_ri = int(tri_ext['max_ri'])  # no right shifting

    # HERE
    # if tri_ext['max_do'] <= max(gi['ld_ss'][0][1], gi['ld_ss'][1][1]):
    # if tri_ext['max_do'] <= extent[-1, 2]:
    #     # diff = max(gi['ld_ss'][0][1], gi['ld_ss'][1][1]) - tri_ext['max_do']
    #     diff = extent[-1, 2] - tri_ext['max_do']
    #     mask_do = int(tri_ext['max_do'] + diff)
    # else:
    #     mask_do = int(tri_ext['max_do'])
    #
    mask_do = int(extent[-1, 2])

    # if tri_max_y < max(gi['ld_start'][1], gi['ld_end'][1]):
    #     # mask_y = int(tri_max_y + min(gi['ld_start'][1], gi['ld_end'][1]))
    #     mask_y = int(tri_max_y + min(gi['ld_start'][1], gi['ld_end'][1]))
    # else:
    #     mask_y = int(tri_max_y)  # no down shifting

    tris = tris_s  # undebug
    return tri_base, tris, tri_ext, mask_ri, mask_do


def shift_triangles(tris, gi, extent_t, tri_ext):
    """
    Perhaps this is only done when objects are out of bounds.
    tris are deepcopied
    OBS shift_do only works currently because the scenario where things have to be shifted up, i.e. when things go
    out of bounds down, is not covered.
    OBS possibly still work to be done here.
    :keywordd
    """

    # SHIFT TRIS DOWN (ONLY COVERS 1/2 SCENARIOS)
    shift_do = extent_t[0, 3] - extent_t[-1, 3]  # INCLUDES SCALING!
    if shift_do > 0:  #
        if tri_ext['max_do'] + shift_do > max(gi['ld_ss'][0][1], gi['ld_ss'][1][1]):
            shift_do = abs(gi['ld_ss'][1][1] - gi['ld_ss'][0][1])  # this means all tris need to be shifted down (base stays at tl 0, 0)
        for i in range(0, len(tris)):
            tri = tris[i]
            tri[0, 1] += shift_do
            tri[1, 1] += shift_do
            tri[2, 1] += shift_do

        tri_ext['min_do'] = np.min([tri[1][1] for tri in tris])
        tri_ext['max_do'] = np.max([tri[0][1] for tri in tris])

    # SHIFT TRIS TO LEFT IF MAX TRI RI EXTENT GOES BEYOND ABSOLUTE BORDER
    shift_hor = 0
    if tri_ext['max_ri'] > gi['max_ri']:  # e.g. case 5: shift left by 100
        shift_hor = gi['max_ri'] - tri_ext['max_ri']

    # SHIFT TRIS TO RIGHT IF MIN_LE IS NEGATIVE (I.E. INVISIBLE) WHILE MI LE IS ALWAYS POSITIVE (ALWAYS VISIBLE)
    elif tri_ext['min_le'] < 0 and min(gi['ld_ss'][0][0], gi['ld_ss'][0][1]) > 0:
        shift_hor = abs(tri_ext['min_le'])  # just to make them positive

    for i in range(0, len(tris)):
        tri = tris[i]
        tri[0, 0] += shift_hor
        tri[1, 0] += shift_hor
        tri[2, 0] += shift_hor
    tri_ext['min_le'] += shift_hor
    tri_ext['max_le'] += shift_hor
    tri_ext['max_ri'] += shift_hor



        # if tri_max_ri + shift_ri > max(gi['ld_start'][0], gi['ld_end'][0]):
        #     shift_ri = gi['ld_end'][0] - gi['ld_start'][0] - tri_max_ri


    # # PROB NEEDS FIXING (WORKS EXCEPT CASE 8)
    # if tri_ext['max_ri'] > max(gi['ld_start'][0], gi['ld_end'][0]):  # triangles want to go too far right
    #     shift_le = -abs(gi['ld_end'][0] - gi['ld_start'][0])
    #     for i in range(0, len(tris)):
    #         tri = tris[i]
    #         tri[0, 0] += shift_le
    #         tri[1, 0] += shift_le
    #         tri[2, 0] += shift_le

    return tris


def shift_triangles_N4(tris, gi, extent_t, tri_ext):
    # SHIFT TRIS DOWN (ONLY COVERS 1/2 SCENARIOS)
    shift_do = extent_t[0, 3] - extent_t[-1, 3]  # INCLUDES SCALING!
    if shift_do > 0:  #
        if tri_ext['max_do'] + shift_do > max(gi['ld_ss'][0][1], gi['ld_ss'][1][1]):
            shift_do = abs(gi['ld_ss'][1][1] - gi['ld_ss'][0][
                1])  # this means all tris need to be shifted down (base stays at tl 0, 0)
        for i in range(0, len(tris)):
            tri = tris[i]
            tri[0, 1] += shift_do
            tri[1, 1] += shift_do
            tri[2, 1] += shift_do

        tri_ext['min_do'] = np.min([tri[1][1] for tri in tris])
        tri_ext['max_do'] = np.max([tri[0][1] for tri in tris])
    else:
        # if tri_ext['max_do'] + shift_do > max(gi['ld_ss'][0][1], gi['ld_ss'][1][1]):
        #     shift_do = abs(gi['ld_ss'][1][1] - gi['ld_ss'][0][
        #         1])  # this means all tris need to be shifted down (base stays at tl 0, 0)
        shift_do = tri_ext['min_do']
        for i in range(0, len(tris)):  # just flipped shift_do
            tri = tris[i]
            tri[0, 1] += -shift_do
            tri[1, 1] += -shift_do
            tri[2, 1] += -shift_do

        tri_ext['min_do'] = np.min([tri[1][1] for tri in tris])
        tri_ext['max_do'] = np.max([tri[0][1] for tri in tris])

    # # SHIFT TRIS TO LEFT IF MAX TRI RI EXTENT GOES BEYOND ABSOLUTE BORDER
    # shift_hor = 0
    # if tri_ext['max_ri'] > gi['max_ri']:  # e.g. case 5: shift left by 100
    #     shift_hor = gi['max_ri'] - tri_ext['max_ri']
    # # elif tri_ext['max_ri'] < gi['max_ri']:
    # #     shift_hor = gi['max_ri'] + tri_ext['max_ri']
    #
    # # SHIFT TRIS TO RIGHT IF MIN_LE IS NEGATIVE (I.E. INVISIBLE) WHILE MI LE IS ALWAYS POSITIVE (ALWAYS VISIBLE)
    # elif tri_ext['min_le'] < 0 and min(gi['ld_ss'][0][0], gi['ld_ss'][0][1]) > 0:
    #     shift_hor = abs(tri_ext['min_le'])  # just to make them positive

    # for i in range(0, len(tris)):
    #     tri = tris[i]
    #     tri[0, 0] += shift_hor
    #     tri[1, 0] += shift_hor
    #     tri[2, 0] += shift_hor
    # tri_ext['min_le'] += shift_hor
    # tri_ext['max_le'] += shift_hor
    # tri_ext['max_ri'] += shift_hor

    # if tri_max_ri + shift_ri > max(gi['ld_start'][0], gi['ld_end'][0]):
    #     shift_ri = gi['ld_end'][0] - gi['ld_start'][0] - tri_max_ri

    # # PROB NEEDS FIXING (WORKS EXCEPT CASE 8)
    # if tri_ext['max_ri'] > max(gi['ld_start'][0], gi['ld_end'][0]):  # triangles want to go too far right
    #     shift_le = -abs(gi['ld_end'][0] - gi['ld_start'][0])
    #     for i in range(0, len(tris)):
    #         tri = tris[i]
    #         tri[0, 0] += shift_le
    #         tri[1, 0] += shift_le
    #         tri[2, 0] += shift_le

    return tris


def gen_extent_normal():
    """
    Only used for spl currently, i.e. for objects that are stationary but grows and shrinks according
    to a scaling sequence that follows something that looks like a normal distribution
    It's currently just set up for set_extent (which might work since it's dark where spls happen), but a
    todo is to merge this into the generic gen_extent function.
    """

    pass


def convert_xy_to_extent(xy, scale_vector, gi, pic):
    '''Cannot use xy_t because it has been shifted partly discarded'''

    # frame_num = gi['frame_ss'][1] - gi['frame_ss'][0]  # ALWAYS

    extent = np.zeros((len(xy), 4))  # left, right, bottom, top borders
    extent_t = np.zeros((len(xy), 4))  # left, right, bottom, top borders

    min_ri = np.min(xy[:, 0])
    min_do = np.min(xy[:, 1])

    w = pic.shape[1]
    h = pic.shape[0]

    for i in range(len(xy)):
        extent[i] = [xy[i][0], xy[i][0] + w * scale_vector[i], xy[i][1], xy[i][1] - h * scale_vector[i]]

    for i in range(len(xy)):
        extent_t[i, 0] = extent[i, 0] - min_ri
        extent_t[i, 1] = extent[i, 1] - min_ri
        extent_t[i, 2] = extent[i, 2] - min_do
        extent_t[i, 3] = extent[i, 3] - min_do



    return extent, extent_t


def rotate_tris(tris, tri_ext, rotation_v):

    max_ri = -99999999999
    max_do = -99999999999

    for i, tri in enumerate(tris):
        tri_mid_x = tri[1, 0]
        tri_mid_y = (tri[1, 1] + tri[0, 1]) / 2

        for j in range(3):

            xy = list(tri[j, :])
            xy_new = rotate_point(origin=(tri_mid_x, tri_mid_y), point=xy, angle=rotation_v[i])
            tri[j, 0] = xy_new[0]
            tri[j, 1] = xy_new[1]

            if xy_new[0] > max_ri:
                max_ri = xy_new[0]
            if xy_new[1] > max_do:
                max_do = xy_new[1]

    tri_ext['max_ri'] = max_ri
    tri_ext['max_do'] = max_do

    return tris, tri_ext


def rotate_point(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def gen_xy_linear(gi):

    """
    Just used by 8 curretnly
    """
    xy = np.zeros(shape=(gi['frames_tot'], 2))

    x_cur = gi['ld'][0]
    y_cur = gi['ld'][1]

    for i in range(0, gi['frames_tot']):

        xy[i, 0] = x_cur
        xy[i, 1] = y_cur

        x_cur = x_cur + gi['v_linear'][0]
        y_cur = y_cur + gi['v_linear'][1]

    if xy[-1, 0] < 0:  # makes sense since they just move left
        raise Exception("bounds. id: " + str(gi['id']))

    return xy


