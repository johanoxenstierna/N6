
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
from src.trig_functions import _normal, _sigmoid, _gamma, _log, _log_and_linear, min_max_normalization

def gen_alpha(g_obj, frames_tot=None, y_range=None, plot=False):
	if frames_tot == None:
		X = np.arange(0, g_obj.gi['frame_ss'][-1] - g_obj.gi['frame_ss'][0])
	else:
		X = np.arange(0, frames_tot)
	alpha = None

	'''NEW'''
	alpha = np.asarray(
		([_sigmoid(x, grad_magn_inv=len(X) / 8, x_shift=3, y_magn=1., y_shift=0) for x in X]))

	alpha = min_max_normalization(alpha, y_range=y_range)

	# if g_obj.__class__.__name__ == 'F':
	# 	'''Has to end at 0 alpha because these include fire smokhs'''
	# 	# alpha = np.full(X.shape, fill_value=0.99)
	# 	# alpha = np.linspace(1, 0, num=len(X))
	# 	# alpha = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 6, x_shift=-2, y_magn=1., y_shift=0) for x in X]))
	# 	# alpha = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 15, x_shift=-2, y_magn=1., y_shift=0) for x in X]))
	# 	# if
	# 	alpha = np.asarray(
	# 		([_sigmoid(x, grad_magn_inv=- len(X) / 5, x_shift=-3, y_magn=1., y_shift=0) for x in X]))
	# 	alpha = min_max_normalization(alpha, y_range=y_range)
	#
	# 	if g_obj.sh.id == '0':
	# 		alpha = np.asarray(
	# 			([_sigmoid(x, grad_magn_inv=- len(X) / 5, x_shift=-3, y_magn=1., y_shift=0) for x in X]))
	# 		alpha = min_max_normalization(alpha, y_range=y_range)
	# 	aa = 5
	# # elif fun_plot == 'spl':
	# # 	# alpha = _gamma(X, mean=3, var=15, y_range=[0.0, 6.0])  # same as extent
	# # 	alpha = _normal(X, mean=len(X)//2, var=len(X)//4, y_range=y_range)  # THIS IS WAVE ALPHA
	# elif g_obj.__class__.__name__ == 'Sp':  #sp2':
	# 	if g_obj.sh.id == '0':
	# 		alpha = np.asarray(
	# 	([_sigmoid(x, grad_magn_inv=- len(X) / 5, x_shift=-3, y_magn=1., y_shift=0) for x in X]))
	# 		alpha = min_max_normalization(alpha, y_range=y_range)
	# 		jj = 7
	# 	elif g_obj.sh.id == '5':
	# 		alpha = np.asarray(
	# 			([_sigmoid(x, grad_magn_inv=- len(X) / 8, x_shift=-3, y_magn=1., y_shift=0) for x in X]))
	# 		alpha = min_max_normalization(alpha, y_range=y_range)
	# 	elif g_obj.sh.id == '7':
	# 		# alpha = _normal(X, mean=len(X) * 0.5, var=len(X) * 0.2, y_range=y_range)  # THIS IS WAVE ALPHA
	# 		alpha = np.asarray(
	# 			([_sigmoid(x, grad_magn_inv=- len(X) / 5, x_shift=-3, y_magn=1., y_shift=0) for x in X]))
	# 	# elif len(X) < 100:  # DEBUG?
	# 	# 	print("HARDCODED ALPHA =================================")
	# 		alpha = np.linspace(y_range[1], y_range[0], num=len(X))
	# 		# alpha[0:int(len(alpha) * 0.3)] = 0.0
	#
	# 	else:
	# 		# alpha = _gamma(X, mean=int(len(X)/60), var=int(len(X)/8), y_range=[0.0, 0.5])  # same as extent. mean=5 gives mean=100 if len == 200
	# 		alpha = _normal(X, mean=len(X) // 2, var=len(X) // 4, y_range=y_range)  # THIS IS WAVE ALPHA
	# elif g_obj.__class__.__name__ == 'C':
	# 	alpha = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 20, x_shift=-18, y_magn=1., y_shift=0) for x in X]))
	# # 	afd = 5

	return alpha




