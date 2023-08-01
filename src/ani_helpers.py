
import cv2
import numpy as np
import random
import P
from scipy.stats import multivariate_normal
from src.trig_functions import min_max_normalization
import matplotlib.transforms as mtransforms

def warp_affine_and_color(ii, ax, im_ax, g_obj):
	"""
	color has to be done here too to avoid multiple removing popping
	ax and im_ax are needed since the ax is removed from im_ax
	g_obj is the info container of the ax (class)
	g_obj is ship, sail or likewise
	Note expl color changes are applied for sails and smokes for the ship that fires.
	Waves have to be sorted out some other way.
	"""

	im_ax[g_obj.index_im_ax].remove()  # BOTH NECESSARY
	im_ax.pop(g_obj.index_im_ax)  # BOTH NECESSARY

	t0 = g_obj.tri_base
	try:
		t1 = g_obj.tris[g_obj.clock]
	except:
		raise Exception("g_obj clock problem  id: " + str(g_obj.id))
	pic_c = g_obj.pic.copy()  # pic with base scale always used.
	# if P.A_STATIC_ALPHA_DARKENING:  # and parent_obj != None:
	# 	static_alpha_darkening(pic_c, ii, g_obj)  # OBS ALSO overwrites the static image AND changes pic copy
	# if P.A_FIRING_BRIGHTNESS:
	# 	if g_obj.__class__.__name__ == 'Smoke':
	# 		if g_obj.hardcoded != True:  # for now?
	# 			pic_c = fire_brightness(pic_c, ii, g_obj)
	# 	else:
	# 		pic_c = fire_brightness(pic_c, ii, g_obj)
	#
	# if P.A_SAIL_HEIGHTS_TROUGHS_TRANSFORM and g_obj.__class__.__name__ == 'Sail':
	# 	g_obj.apply_heights_troughs_transform(pic_c, ii)  # changes the pic copy

	M = cv2.getAffineTransform(t0, t1)
	dst = cv2.warpAffine(pic_c, M, (int(g_obj.tri_ext['max_ri']), int(g_obj.tri_ext['max_do'])+0))
	# dst = cv2.warpAffine(pic_c, M, (152, 89))

	# DOESNT WORK, use rotate_tris =======
	# center = (5, 5) #(pic_c.shape[1] // 2, pic_c.shape[0] // 2)
	# # center = (g_obj.tri_ext['max_ri'], g_obj.tri_ext['max_do'])
	# angle = g_obj.rotation_v[g_obj.clock]
	# scale = 1
	# rot_mat = cv2.getRotationMatrix2D(center, angle, scale)  # DOESNT WORK. USE rotate_tris
	# M = rot_mat
	# dst = cv2.warpAffine(pic_c, M, (int(g_obj.tri_ext['max_ri']), int(g_obj.tri_ext['max_do']) + 0))

	img = np.zeros((g_obj.mask_do, g_obj.mask_ri, 4))  # new image inited
	try:
		img[img.shape[0] - dst.shape[0]:, img.shape[1] - dst.shape[1]:, :] = dst  # lower right is filled
	except:
		adf = 5

	im_ax.insert(g_obj.index_im_ax, ax.imshow(img, zorder=g_obj.gi['zorder'], alpha=1))
	g_obj.ax1 = im_ax[g_obj.index_im_ax]


def mpl_affine(ii, g_obj, ax0, im_ax):

	""""""
	if g_obj.id[2] == 'f':  # legacy
		if g_obj.id[0] in ['0', '5']:
			M = mtransforms.Affine2D(). \
				    scale(g_obj.scale_vector[g_obj.clock], -g_obj.scale_vector[g_obj.clock]). \
				    rotate(g_obj.rotation_v[g_obj.clock]). \
				    translate(g_obj.gi['ld'][0], g_obj.gi['ld'][1]) + ax0.transData
		elif g_obj.id[0] in ['6']:
			try:
				M = mtransforms.Affine2D(). \
					    scale(g_obj.scale_vector[g_obj.clock], -g_obj.scale_vector[g_obj.clock]). \
					    rotate(g_obj.rotation_v[g_obj.clock]). \
					    translate(g_obj.gi['ld'][0] + g_obj.gi['x_mov'][g_obj.clock], g_obj.gi['ld'][1]) + ax0.transData
			except:
				adf = 6
		elif g_obj.id[0] in ['1']:  # YES, 1 has f shockwave
			M = mtransforms.Affine2D(). \
				    scale(g_obj.scale_vector[g_obj.clock], -g_obj.scale_vector[g_obj.clock]). \
				    rotate(g_obj.rotation_v[g_obj.clock]). \
				    translate(g_obj.gi['ld'][0] + g_obj.gi['x_mov'][g_obj.clock],
			                  g_obj.gi['ld'][1] + g_obj.gi['y_mov'][g_obj.clock]) + ax0.transData
	elif g_obj.id[2:4] == 'sr':
		M = mtransforms.Affine2D(). \
			    scale(g_obj.scale_vector[g_obj.clock], -g_obj.scale_vector[g_obj.clock]). \
			    rotate(g_obj.rotation_v[g_obj.clock]). \
			    translate(g_obj.xy[g_obj.clock][0], g_obj.xy[g_obj.clock][1]) + ax0.transData
	elif g_obj.id[2] == 'r':
		M = mtransforms.Affine2D(). \
			    rotate_around(4, 6, g_obj.rotation_v[g_obj.clock]). \
			    scale(g_obj.scale, -g_obj.scale). \
			    translate(g_obj.xy[g_obj.clock][0], g_obj.xy[g_obj.clock][1]) + ax0.transData
	elif g_obj.id[2] == 'l':
		M = mtransforms.Affine2D(). \
			    rotate_around(4, 6, g_obj.gi['rad_rot']). \
			    scale(g_obj.gi['scale'], -g_obj.gi['scale']). \
			    translate(g_obj.gi['ld'][0], g_obj.gi['ld'][1]) + ax0.transData

	g_obj.ax1.set_transform(M)


def decrement_all_index_im_ax(index_removed, shs, waves=None):
	"""
	Whenever an im_ax is popped from the list, all index_im_ax with higher index will be wrong and
	need to be decremented by 1.
	"""

	for sh in shs.values():
		if sh.index_im_ax != None:
			if sh.index_im_ax > index_removed:
				sh.index_im_ax -= 1
		for f in sh.fs.values():
			if f.index_im_ax != None:
				if f.index_im_ax > index_removed:
					f.index_im_ax -= 1

			for sp_key, sp in f.sps.items():  # OBS THIS MEANS sps must have same or fewer frames than f
				if sp.index_im_ax != None:
					if sp.index_im_ax > index_removed:
						sp.index_im_ax -= 1

		'''
		HUGE BUG HERE
		DANGER: THIS SEEMS TO MESS UP ABOVE: SOLUTION: ALWAYS HAVE SP AS CHILD OF SR
		'''
		for sp_key, sp in sh.sps.items():
			if sp.index_im_ax != None and sp.f == None:
				if sp.index_im_ax > index_removed:
					sp.index_im_ax -= 1


def set_sps(sp, im_ax, ii, ax0):

	if sp.ars_bool == 0:  # NOT ON GROUND
		sp_len_cur = sp.sp_lens[sp.clock]

		if sp.gi['special']:
			if sp.clock > 999:
				raise Exception("todo maybe")

		if sp.clock < sp_len_cur + 1:  # beginning
			xys_cur = [sp.xy[:sp.clock, 0], sp.xy[:sp.clock, 1]]
		else:
			xys_cur = [sp.xy[sp.clock:sp.clock + sp_len_cur, 0], sp.xy[sp.clock:sp.clock + sp_len_cur, 1]]

		sp.ars_bool = check_ars(xys_cur, ii)
		# im_ax[sp.index_im_ax].set_data(xys_cur[0], xys_cur[1])  # SELECTS A SUBSET OF WHATS ALREADY PLOTTED

		# if P.ARS == 0:  # otherwise
		im_ax[sp.index_im_ax].set_data(xys_cur)  # SELECTS A SUBSET OF WHATS ALREADY PLOTTED

		# try:
		im_ax[sp.index_im_ax].set_color((sp.R[sp.clock], sp.G[sp.clock], sp.B[sp.clock]))

		if P.ARS == 1:  # only show once on ground
			im_ax[sp.index_im_ax].set_alpha(0)
		else:
			im_ax[sp.index_im_ax].set_alpha(sp.alphas[sp.clock])
		# except:
		# 	extra_out = ''
		# 	if sp.f != None:
		# 		extra_out = sp.f.id
		# 	raise Exception(
		# 		"im_ax[sp.index_im_ax].set_color((sp.R[sp.clock], sp.G[sp.clock], sp.B[sp.clock])) " + str(sp.id) + \
		# 		' ' + extra_out)

	else:  # ON GROUND
		'''Override FRAME_SS'''
		# pass
		if P.ARS == 0:  # in air
			'''Ok. So conclusion. Good for future but it wont work in this case cuz one d had to create class 
			instance stump copies of the sp in the air and also modify when stuff gets plotted, to reap the savings.
			Instead, in this case each arrow gets its own class instance and theyre all kept till the end. If this 
			eats too much time (due to the remove from im_ax thing, then do the class stump thing
			REVOLUTION: IM_AX2'''
			sp.frame_ss[1] = ii + 1  # i.e. it will be removed next frame, so this is last set_data

		else:  # on ground
			sp.frame_ss[1] = P.FRAMES_STOP - 1
			im_ax[sp.index_im_ax].set_alpha(1)
		#
		# '''Probably needs to be added to im_ax. Each ars is a plot command.
		# Anyways, create a new plot for ars and then no need to set_data, sfbi'''
		# # ax0.plot(sp.xy[:, 0], sp.xy[:, 1], zorder=100, alpha=1, color='white')  # (sp.R[0], sp.G[0], sp.B[0])
		# ax0.plot([50, 100], [200, 300], zorder=100, alpha=1, color='white')  # (sp.R[0], sp.G[0], sp.B[0])

		'''HERE. add xys_cur to ars. ars just plots all the xys_cur '''




def check_ars(xys_cur, ii):

	# if len(xys_cur[0]) < 1:
	# 	return 1
	# elif xys_cur[0][-1] > 660:
	# 	return 2

	if ii > 196:
		return 1

	return 0


def add_to_ars(sp, im_ax):

	'''The main point of this is not to achieve any animation speed-up, which it wont, but rather
	to make things more sensical.'''

	'''Here add xy limit condition to see whether the arrow is actually relevant for ars'''

	aa = 5


