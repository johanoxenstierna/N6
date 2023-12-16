


from scipy.stats import chi2
from scipy.stats import norm, gamma, multivariate_normal
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines

import math
import numpy as np
import P as P
import random


def _normal(X, mean, var, y_range):
	# Y = norm.pdf(X, loc=len(X)//2, scale=10)
	Y = norm.pdf(X, loc=mean, scale=var)
	Y = min_max_normalization(Y, y_range)
	return Y


def _gamma(X, mean, var, y_range):
	Y = gamma.pdf(X, mean, 0, var)
	Y = min_max_normalization(Y, y_range=y_range)
	return Y


def _log(X, y_range):
	Y = np.log(X)
	Y = min_max_normalization(Y, y_range=y_range)
	return Y


def _log_and_linear(X, y_range):  # hardcoded for now since only used for smoka
	Y = 0.99 * np.log(X) + 0.01 * X
	Y = min_max_normalization(Y, y_range=y_range)
	return Y


def min_max_normalization(X, y_range):

	"""

	"""

	new_min = y_range[0]
	new_max = y_range[1]
	Y = np.zeros(X.shape)

	_min = np.min(X)
	_max = np.max(X)

	for i, x in enumerate(X):
		Y[i] = ((x - _min) / (_max - _min)) * (new_max - new_min) + new_min

	return Y

# def sigmoid(X):
# 	return 1/(1 + np.exp(-X))

def _sigmoid(x, grad_magn_inv=None, x_shift=None, y_magn=None, y_shift=None):
	"""
	the leftmost dictates gradient: 75=steep, 250=not steep
	the rightmost one dictates y: 0.1=10, 0.05=20, 0.01=100, 0.005=200
	y_magn???
	"""
	return (1 / (math.exp(-x / grad_magn_inv + x_shift) + y_magn)) + y_shift  # finfin


# def _xy_projectile(X, v, theta):
#
# 	"""To"""
#
# 	# xy = np.zeros((100, 2))  # MIDPOINT
#
# 	G = 9.8
#
# 	t_flight = 0.1 * v * np.sin(theta) / G
# 	t = np.linspace(0, t_flight, len(X))
#
# 	x = v * np.cos(theta) * t
# 	y = v * np.sin(theta) * 1 * t - 0.5 * G * t ** 2
#
# 	ax.plot(X, x, '-', color='blue')
# 	ax.plot(X, y, '-', color='red')
# 	adf = 5


def sin_exp_experiment(X):
	"""
	Extension of cph. Firing frames is a combination of a number of normal distributions with specified nums and
	means in firing_info.
	"""

	cycles_currently = P.FRAMES_TOT / (2 * np.pi)
	# d = cycles_currently / P.EXPL_CYCLES  # divisor_to_achieve_cycles
	d = cycles_currently / P.EXPL_CYCLES  # divisor_to_achieve_cycles

	f_0 = 0.2  # firing prob coefficients
	f_1 = 0.05
	f_2 = 0.4

	left_shift = random.randint(int(-P.FRAMES_TOT), 0)
	Y = (f_0 * np.sin((X + left_shift) / d) +  # fast cycles
	     f_1 * np.sin((X + left_shift - 0) / (3 * d)) +  # slow cycles
	     f_2 * np.log((X + 10) / d) / np.log(P.FRAMES_TOT)) - 0.1  # prob of firing
	# Y = np.clip(Y, 0.0, 0.8)

	# Y = (2 * np.sin(X) + 0.5 * np.sin(X) + 0.4 * np.log(X) / np.log(len(X))) - 0.1

	return Y


def temperature_for_optimization(X):
	"""
	X is a list of
	"""
	T = np.zeros((2000,))
	t_cur = 10000
	d = 0.996
	for i in range(2000):
		T[i] = t_cur
		t_cur = t_cur * d

	delta = 200
	Y = np.exp(-abs(delta) / T)

	return Y


if __name__ == '__main__':

	fig, ax = plt.subplots(figsize=(10, 6))

	# SMOKE ============
	# X = np.arange(0, 720, 1)  # large: 960
	# Y = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 10, x_shift=-6, y_magn=1., y_shift=0.4) for x in X]))  # smoka alpha
	# X = X + 1
	# # Y = _log(X) #  SMOKR
	# Y = _log_and_linear(X) #  SMOKA

	# # # FIr: ===================
	# X = np.arange(0, 240, 1)  # large: 960
	# tot_num = 110
	# Y0 = _normal(X, mean=40, var=30, y_range=[0, 1])
	# num0 = 20
	# Y1 = _normal(X, mean=170, var=30, y_range=[0, 1])
	# num1 = 40
	# YS = [Y0, Y1]
	# Y = (num0 / tot_num) * YS[0] + (num1 / tot_num) * YS[1]
	# Y = Y / np.sum(Y)
	# aa = np.random.choice(range(len(Y)), size=50, p=Y)
	# aa.sort()

	'''
	Need do create candidate list and check mass and see whether there are too many 
	fires per moving average unit. 
	'''

	# # # # WAVE alpha NOT EXPL! ALpha 1 in beg cuz it starts real small ============
	X = np.arange(1, 401)
	# # # Y = _normal(X, mean=len(X) // 2, var=len(X) // 4, y_range=[0, 0.15])  # alpha
	# Y = ([_sigmoid(x, grad_magn_inv=-len(X) / 12, x_shift=-4, y_magn=22, y_shift=0) for x in X])  # expl alpha
	# Y = np.asarray([_sigmoid(x, grad_magn_inv=-len(X) / 10, x_shift=-2, y_magn=40, y_shift=0) for x in X])  # expl alpha
	# Y = np.asarray([_sigmoid(x, grad_magn_inv=-len(X) / 12, x_shift=-4, y_magn=22, y_shift=0) for x in X])  # expl alpha
	# aa = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 10, x_shift=-2, y_magn=40, y_shift=0) for x in X]))
	# adf = 5

	# Y = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 30, x_shift=-1, y_magn=1., y_shift=0) for x in X]))  # F
	# Y = _gamma(X, mean=2, var=20, y_range=[0.01, 1])
	# _xy_projectile(X, v=20, theta=0.2)
	# External: Test for sigmoid for probability

	# Y = np.asarray(([_sigmoid(x, grad_magn_inv=-len(X) / 10, x_shift=1, y_magn=20, y_shift=0) for x in X]))
	# Y = np.asarray(([_sigmoid(x, grad_magn_inv=len(X)/10, x_shift=5, y_magn=4, y_shift=0.05) for x in X]))

	# Y = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 50, x_shift=-18, y_magn=1., y_shift=0) for x in X]))

	# Y = [x/sum(Y) for x in Y]
	# # gg = np.sum(Y)
	# gg = 5

	'''Temperature experiment'''
	# Y = temperature_for_optimization(X)

	# ## WAVE expl (X is distance and Y is alpha) ==============
	# X = np.arange(0, 1000, 1)  # large: 960
	# Y = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 10, x_shift=-2, y_magn=6.2, y_shift=0) for x in X]))
	# aa = 5

	# # SP extent =============
	# X = np.arange(0, 50)
	# Y = _normal(X, mean=1, var=5, y_range=[0, 0.999])

	# SP ALPHA ===========
	Y = np.asarray(
		([_sigmoid(x, grad_magn_inv=len(X) / 8, x_shift=3, y_magn=1., y_shift=0) for x in X]))

	Y2 = np.sin((X - 20) / 16) / 4

	Y = Y + Y2
	# Y = Y2

	# 5 SR ALPHA ==============
	# Y = np.asarray(
	# 	([_sigmoid(x, grad_magn_inv=- len(X) / 8, x_shift=-3, y_magn=1., y_shift=0) for x in X]))

	# F ALPHA ============
	# Y = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 15, x_shift=-2, y_magn=1., y_shift=0) for x in X]))

	# SP dots: ld_offset. input is ld_offset_scale. output is offset (needs scaling afterwards)
	# Y = np.asarray(([_sigmoid(x, grad_magn_inv= -30, x_shift=-3, y_magn=1, y_shift=0) for x in X]))
	# Y = min_max_normalization(Y, y_range=[0, 1])

	# STORAGE ASSIGNMENT NUMBER OF SWAPS
	# Y = np.asarray(
	# 	([_sigmoid(x, grad_magn_inv=-1, x_shift=-4, y_magn=2, y_shift=0) for x in X]))
	# p = np.asarray([x / sum(Y) for x in Y])

	# FALLING OBJECT X motion
	# Y = 2 * np.log(X)
	# input = np.linspace(0, 4, num=len(X))
	# Y = np.exp(input)  # X motion

	# distribute frames


	'''EXECUTE'''
	ax.plot(X, Y, '-')
	# plt.xlim([-5, NUM])
	# plt.ylim([-2.5, 2.5])




	plt.show()
