
import cv2
import numpy as np
import random
import P
from scipy.stats import multivariate_normal
from src.trig_functions import min_max_normalization
import matplotlib.transforms as mtransforms

def decrement_all_index_axs0(index_removed, shs, waves=None):
	"""
	Whenever an axs0 is popped from the list, all index_axs0 with higher index will be wrong and
	need to be decremented by 1.
	"""

	for sh in shs.values():
		if sh.index_axs0 != None:
			if sh.index_axs0 > index_removed:
				sh.index_axs0 -= 1
		for f in sh.fs.values():
			if f.index_axs0 != None:
				if f.index_axs0 > index_removed:
					f.index_axs0 -= 1

			for sp_key, sp in f.sps.items():  # OBS THIS MEANS sps must have same or fewer frames than f
				if sp.index_axs0 != None:
					if sp.index_axs0 > index_removed:
						sp.index_axs0 -= 1

		'''
		HUGE BUG HERE
		DANGER: THIS SEEMS TO MESS UP ABOVE: SOLUTION: ALWAYS HAVE SP AS CHILD OF SR
		'''
		for sp_key, sp in sh.sps.items():
			if sp.index_axs0 != None and sp.f == None:
				if sp.index_axs0 > index_removed:
					sp.index_axs0 -= 1


def set_sps(sp, axs0, axs1, ax_b, ii):

	# if sp.ars_bool == 0:  # NOT ON GROUND
	sp_len_cur = sp.sp_lens[sp.clock]

	# PEND DEL if sp.gi['special']:
	# 	if sp.clock > 999:
	# 		raise Exception("todo maybe")

	if sp.clock < sp_len_cur + 1:  # beginning
		xys_cur = [sp.xy[:sp.clock, 0], sp.xy[:sp.clock, 1]]  # list with 2 cols
	else:
		xys_cur = [sp.xy[sp.clock:sp.clock + sp_len_cur, 0], sp.xy[sp.clock:sp.clock + sp_len_cur, 1]]

	ars_bool = sp.check_ars(xys_cur, ii)  # SHOULD BE PRE

	axs0[sp.index_axs0].set_data(xys_cur)  # SELECTS A SUBSET OF WHATS ALREADY PLOTTED
	axs0[sp.index_axs0].set_color((sp.R[sp.clock], sp.G[sp.clock], sp.B[sp.clock]))
	axs0[sp.index_axs0].set_alpha(sp.alphas[sp.clock])

	if ars_bool == 1:  # on ground
		xys_cur = sp.adjust_ars(xys_cur)  # obs this overwrites it
		sp.frame_ss[1] = ii + 1  # i.e. it will be removed next frame, so this is last set_data
		# '''OBS in this project an f lasts the whole time. But better could have been to wait for all '''
		axs1.append(ax_b.plot(xys_cur[0], xys_cur[1], zorder=sp.gi['zorder'],
		                     alpha=sp.alphas[sp.clock], color=(sp.R[sp.clock], sp.G[sp.clock], sp.B[sp.clock]))[0])

# def check_ars(xys_cur, ii):
#
# 	"""Use the tip of arrow"""
#
# 	if len(xys_cur[0]) < 1:
# 		return 0
#
# 	if xys_cur[0][-1] > 0 and xys_cur[0][-1] < 1280:
# 		# ARS_Y_OFFSET = random.randint(-70, 10)
#
# 		if xys_cur[1][-1] > 550 and random.random() < 0.33:  # checks y
# 			return 1
#
# 	return 0


def add_to_ars(sp, axs0):

	'''The main point of this is not to achieve any animation speed-up, which it wont, but rather
	to make things more sensical.'''

	'''Here add xy limit condition to see whether the arrow is actually relevant for ars'''

	aa = 5


