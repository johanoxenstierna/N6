
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

		for sr in sh.srs.values():
			if sr.index_im_ax != None:
				if sr.index_im_ax > index_removed:
					sr.index_im_ax -= 1

		for r in sh.rs.values():
			if r.index_im_ax != None:
				if r.index_im_ax > index_removed:
					r.index_im_ax -= 1

		# for l in sh.ls.values():
		# changed from dict to list
		for l in sh.ls:
			if l.index_im_ax != None:
				if l.index_im_ax > index_removed:
					l.index_im_ax -= 1

		for li in sh.lis:
			if li.index_im_ax != None:
				if li.index_im_ax > index_removed:
					li.index_im_ax -= 1

		for c in sh.cs.values():
			if c.index_im_ax != None:
				if c.index_im_ax > index_removed:
					c.index_im_ax -= 1


def set_sps(sp, im_ax):

	if sp.clock < sp.gi['sp_len'] + 1:  # TODO: CHANGE THIS TO EXTERNAL FUNCTION
		im_ax[sp.index_im_ax].set_data(sp.xy[:sp.clock, 0], sp.xy[:sp.clock, 1])
	else:
		im_ax[sp.index_im_ax].set_data(sp.xy[sp.clock - sp.gi['sp_len']:sp.clock, 0],
		                               sp.xy[sp.clock - sp.gi['sp_len']:sp.clock, 1])
	try:
		im_ax[sp.index_im_ax].set_color((sp.R[sp.clock], sp.G[sp.clock], sp.B[sp.clock]))
		im_ax[sp.index_im_ax].set_alpha(sp.alphas[sp.clock])
	except:
		extra_out = ''
		if sp.f != None:
			extra_out = sp.f.id
		raise Exception("im_ax[sp.index_im_ax].set_color((sp.R[sp.clock], sp.G[sp.clock], sp.B[sp.clock])) " + str(sp.id) + \
		                ' ' + extra_out)



# for smokr in sh.smokrs.values():
# 	if smokr.index_im_ax != None:
# 		if smokr.index_im_ax > index_removed:
# 			smokr.index_im_ax -= 1
# for expl in sh.expls.values():
# 	if expl.index_im_ax != None:
# 		if expl.index_im_ax > index_removed:
# 			expl.index_im_ax -= 1
# for spl in ship.spls.values():
# 	if spl.index_im_ax != None:
# 		if spl.index_im_ax > index_removed:
# 			spl.index_im_ax -= 1

# for wave in waves.values():
# 	if wave.index_im_ax != None:
# 		if wave.index_im_ax > index_removed:
# 			wave.index_im_ax -= 1


# def


# def static_alpha_darkening(pic, ii, g_obj):
# 	"""
# 	R   G   B   !   !   !
# 	https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
#
# 	Works by overwriting the image in memory. If alpha set to 0 in beginning it cannot be restored!
# 	The specified amount is always in relation to latest written image!
# 	The sails are done manually.
#
# 	Might get super expensive to do this for ships at each frame. FIXED: doing it statically at certain frames
# 	expl_at_coords: coordinates where there are active expls this frame (the expl "event" continues more frames
# 	than the expl is shown).
#
# 	Not applied for expls
#
# 	"""
# 	if g_obj.__class__.__name__ not in ['Sail', 'Smoke', 'Ship']:  #  INCLUDED ones. WAVE DONE ELSEWHERE
# 		return pic
#
# 	if g_obj.__class__.__name__ == 'Ship':
# 		gi = g_obj.gi
# 		ab_clock = g_obj.ab_clock
# 	else:
# 		gi = g_obj.ship.gi
# 		ab_clock = g_obj.ship.ab_clock
#
# 	ship_ab_at_clock = gi['alpha_and_bright'][ab_clock]  # this is incremented for ship at bottom of animation loop
# 	if ii == ship_ab_at_clock[0]:  # hence this is checked every frame but only runs once for each obj
#
# 		c = 1
# 		if g_obj.__class__.__name__ == 'Smoke':  # needed since smokas are updated too rarely otherwise\
# 			if g_obj.type == 'a':
# 				c = 0.98  # visible switch if less than 0.98
#
# 			if random.random() < 0.3:  # also add darkening effect (red layer decreased)
# 				c = 0.98
# 				g_obj.pic[:, :, 0] = g_obj.pic[:, :, 0] * ship_ab_at_clock[2] * c
#
# 		g_obj.pic[:, :, 1] = g_obj.pic[:, :, 1] * ship_ab_at_clock[2] * c
# 		g_obj.pic[:, :, 2] = g_obj.pic[:, :, 2] * ship_ab_at_clock[2] * c
#
# 		if g_obj.__class__.__name__ != 'Smoke':  # alpha only for ships
# 			g_obj.pic[:, :, 3] = g_obj.pic[:, :, 3] * ship_ab_at_clock[1] * c
#
# 		# g_obj.pic[:, :, 1] = g_obj.pic[:, :, 1] * g_obj.ab_cur[1]  # failed attempt at fixing it
# 		# g_obj.pic[:, :, 2] = g_obj.pic[:, :, 2] * g_obj.ab_cur[1]
# 		# g_obj.pic[:, :, 3] = g_obj.pic[:, :, 3] * g_obj.ab_cur[0]
#
# 		g_obj.ab_cur[0] *= ship_ab_at_clock[1]  # needed for smokes
# 		g_obj.ab_cur[1] *= ship_ab_at_clock[2]  # needed for smokes
# 		# THESE PROBABLY NEED TO BE SET FOR ALL OF THEM, NOT JUST THE ONES THAT ARE CURRENTLY DRAWN (KEPT FOR NOW DUE TO OKISH RANDOM EFFECT).
# 		# THIS IS ALSO REASON WHY SMOKAS NEED EXTRA
#
# 		aa = 6
#
#
# def hardcoded_adjustments(g_obj, ii):
#
# 	"""assumed to be a ship for now"""
#
# 	if g_obj.id == "0" and ii > 3600:
# 		g_obj.gi['xtras']['0_a_0']['scale_ss'][1] = 0.9
# 		g_obj.gi['xtras']['0_a_1']['scale_ss'][1] = 0.7
# 		g_obj.gi['xtras']['0_a_2']['scale_ss'][1] = 0.9
# 		g_obj.gi['xtras']['0_smokrs']['scale_max'] = 0.9
#
# 	aa = 5




# if g_obj.__class__.__name__ == 'Smoke':
# 	if ii == 13:
# 		adf = 5
# 	if g_obj.hardcoded == True:  # OBS SMOKRS HAVE BE CHANGED GLOBALLY (NOT POSSIBLE OTHERWISE)
# 		return pic  # no static darkenign for hardcoded smokas (the ones that are not launched randomly
# 	if g_obj.drawn == 1:  # STATIC DARKN ONLY WHEN PIC IS FIRST DRAWN
# 		pass  # TODO REPLACE WITH GLOBAL ALPHA DARKENING PARAMETER IN P

# REPLACED WITH ab_cur
# ship_ab_at_clock_prev = g_obj.ship.gi['alpha_and_bright'][0]  # this is needed since ship_ab_at_clock is incremented after the first ii hit.
# for i in range(1, len(g_obj.ship.gi['alpha_and_bright'])):  # finds previous alpha_and_bright
# 	if ii <= g_obj.ship.gi['alpha_and_bright'][i][0]:
# 		break
# 	else:
# 		ship_ab_at_clock_prev = g_obj.ship.gi['alpha_and_bright'][i]

# g_obj.pic[:, :, 0] = g_obj.pic[:, :, 0]  # * ship_ab_at_clock[2]
# g_obj.pic[:, :, 1] = g_obj.pic[:, :, 1] * g_obj.ship.ab_cur[1]
# g_obj.pic[:, :, 2] = g_obj.pic[:, :, 2] * g_obj.ship.ab_cur[1]
# g_obj.pic[:, :, 3] = g_obj.pic[:, :, 3] * g_obj.ship.ab_cur[0]

# HSV (perhaps not needed)
# img = ship_pic
# hsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
# h, s, v = cv2.split(hsv)
# v += value
# final_hsv = cv2.merge((h, s, v))
# img2 = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
# img[:, :, 0:3] = img2
#
# # think this is just the operation to sort out alpha
# idx0 = np.argwhere(img[:, :, 0:3] < 0.0)
# idx1 = np.argwhere(img[:, :, 0:3] > 1.0)
#
# for row, col, ch in idx0:
# 	img[row, col, ch] = 0.0
#
# for row, col, ch in idx1:
# 	img[row, col, ch] = 1.0

# return pic


# def fire_brightness(pic, ii, g_obj):
# 	"""Instant lightning up of ship objects when firing"""
#
# 	type = 'constant'
# 	gi = None
# 	# expls = None
# 	if g_obj.__class__.__name__ == 'Ship':
# 		gi_ship = g_obj.gi
# 		# expls = g_obj.expls
# 		type = 'mvn'  # multivariate normal
# 	else:
# 		gi_ship = g_obj.ship.gi
# 	# expls = g_obj.ship.expls
#
# 	# FIRING UPDATES = ===================
# 	if ii not in gi_ship['firing_frames'] or g_obj.__class__.__name__ not in ['Ship', 'Sail', 'Wave', 'Spl', 'Expl', 'Smoke']:
# 		return pic
#
# 	# BRIGHTNESS =
# 	if type == 'constant':  # same shift applied to whole pic
# 		# ex = 5.84
#
# 		c = 0.5
# 		if g_obj.__class__.__name__ == 'Smoke':
# 			if g_obj.type == 'r':
# 				c = 1
# 			elif g_obj.type == 'a':  # SMOKHS do not come here
# 				c = 0.2  # 50: 0.3  doesnt work for larger smokas
# 				if g_obj.id_gi in ['0_a_2', '2_a_3', '1_a_2', '5_a_1', '6_a_1', '6_a_2', '6_a_3', '7_a_2']:  # 51: new
# 					c = 0.03
# 		elif g_obj.__class__.__name__ == 'Sail':
# 			c = 0.4  # 47 ex was 0.4
# 		elif g_obj.__class__.__name__ == 'Wave':
# 			c = 0.7  # 44 ex was 1.5
#
# 		ex = c * np.random.rand() + 1  # TODO: Perhaps make this more fancy.  2.7 makes it totally white
#
# 		# if iii in firing_frames:
# 		# 	ex = 0.84  # decrease in green and blue
# 		# pic = _s.pic.copy()  # REQUIRED
# 		pic[:, :, 0] = pic[:, :, 0] * ex  # more y=more red, less=more green
# 		pic[:, :, 0][pic[:, :, 0] > 1.0] = 1.0
# 		pic[:, :, 1] = pic[:, :, 1] * ex  # more y=more green, less=more red
# 		pic[:, :, 1][pic[:, :, 1] > 1.0] = 1.0
# 		pic[:, :, 2] = pic[:, :, 2] * ex  # Needed to complement red and green
# 		pic[:, :, 2][pic[:, :, 2] > 1.0] = 1.0
# 	elif type == 'mvn':
# 		X0, X1 = np.meshgrid(np.arange(0, pic.shape[1], 1), np.arange(0, pic.shape[0], 1))
# 		X = np.dstack((X0, X1))
#
# 		# Select ld for mean
# 		ld = gi_ship['xtras'][gi_ship['id'] + '_expls']['ld_offset_ss'][0].copy()  # OMG actually gets overwritten
# 		ld[0] += random.randint(-gi_ship['xtras'][gi_ship['id'] + '_expls']['ld_offset_rand_ss'][0][0],
# 								gi_ship['xtras'][gi_ship['id'] + '_expls']['ld_offset_rand_ss'][0][0])
# 		ld[1] += random.randint(-gi_ship['xtras'][gi_ship['id'] + '_expls']['ld_offset_rand_ss'][0][1],
# 								gi_ship['xtras'][gi_ship['id'] + '_expls']['ld_offset_rand_ss'][0][1])
# 		left_top = ld
# 		left_top[1] = pic.shape[0] + ld[1]
#
# 		# Y = multivariate_normal.pdf(X, mean=(72, 213), cov=[[50, 0], [0, 50]])
# 		Y = multivariate_normal.pdf(X, mean=left_top, cov=[[pic.shape[1] * 1.2, 0], [0, pic.shape[0] * 1.2]])  # 350. 650
# 		Y = min_max_normalization(Y, y_range=[0, 0.4])  # this is amount added to current
#
# 		# aa = pic[:, :, 0] * Y
# 		pic[:, :, 0] += Y  # more y=more red, less=more green
# 		pic[:, :, 0][pic[:, :, 0] > 1.0] = 1.0
# 		pic[:, :, 1] += Y  # more y=more green, less=more red
# 		pic[:, :, 1][pic[:, :, 1] > 1.0] = 1.0
# 		pic[:, :, 2] += Y  # Needed to complement red and green
# 		pic[:, :, 2][pic[:, :, 2] > 1.0] = 1.0
#
# 	return pic

#
# def find_all_ax_at_coord():  # probably wont be used
#
# 	return ""

