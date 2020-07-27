'''
This module reads all .mat rectified files in "interactive_rectified/" and produces the corresponding .pfm and .npy files, with padded missing pixels

'''

import os
import numpy as np
import scipy.io as io
import glob
import matplotlib.pyplot as plt
from pfm_lib import save_pfm

def compute_occup_prob(x,m,b):
	# params
	t_thres = 300
	col_start = 125
	
	# corner img
	x_corner = x[0:t_thres,:]
	
	# sizes
	height = x_corner.shape[0]
	width = x_corner.shape[1]
	
	n_pixels=0.0
	n_occupied=0.0
	for col in range(0,width):
		# check for start range
		if col>=125:
			for row in range(0,height):
				row_thres = np.floor(m * col + b)
				# check if above the line
				if row > row_thres:
					n_pixels = n_pixels + 1
					# check if occupied
					if x_corner[row,col]>0:
						n_occupied = n_occupied+1
	
	prob= n_occupied / n_pixels
	return prob


if __name__=='__main__':
	src_dir = 'interactive_rect/'
	filepaths = glob.glob(src_dir+'*.mat')
	
	# pngs dir for video
	dest_dir = 'interactive_rect_pad/'
	if not os.path.exists(dest_dir):
		os.mkdir(dest_dir)
	
	# define diag line x=m*y+b
	row_cut_1 = 340.0
	row_cut_2 = 47.0
	col_cut_1 = 0.0
	col_cut_2 = 1024.0
	m = (row_cut_2 - row_cut_1) / (col_cut_2 - col_cut_1)
	b = row_cut_1 - m * col_cut_1	

	for filepath in filepaths:
		# load
		f = io.loadmat(filepath)
		x = f['data']
		x_res = np.reshape(x, (1024,1024))
		
		# compute occupancy prob using diag line above
		prob = compute_occup_prob(x_res, m, b)
		
		# fill image via binomial sampling
		x_padded = x_res
		for col in range(0,1024):
			row_thres = int(np.floor(m*col+b))
			pad_size = row_thres
			occup_ar = np.random.binomial(1, prob, size=pad_size) # sample 1 with probability prob
			x_padded[0:row_thres, col] = occup_ar
		
		# format
		path, name_mat = filepath.split('\\')
		name, ext = name_mat.split('.')
		
		# save
		save_pfm(dest_dir+name+'.pfm', x_padded) #save in 2D
		#np.save(dest_dir+name+'.npy',  x)      #save in 3D
	#plt.imshow(x_padded, vmax=2)
	#plt.show(block=True)