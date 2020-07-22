'''
This module reads all .mat rectified files in "interactive_rectified/" and produces the corresponding .pfm and .npy files

'''

import numpy as np
import scipy.io as io
import glob
from pfm_lib import save_pfm

if __name__=='__main__':
	data_dir = 'interactive_rectified/'
	filepaths = glob.glob(data_dir+'*.mat')
	
	for filepath in filepaths:
		# load
		f = io.loadmat(filepath)
		x = f['data'] # (1024,32,32)
		
		# reshape
		x_res = np.reshape(x, (1024,1024))
		
		# format
		path, name_mat = filepath.split('\\')
		name, ext = name_mat.split('.')
		
		# save
		save_pfm(data_dir+name+'.pfm', x_res) #save in 2D
		np.save(data_dir+name+'.npy',  x)      #save in 3D