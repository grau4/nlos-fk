'''
This module reads the pfm files of a sequence and renders a video

Author: Javier Grau
'''

import os
import numpy as np
import cv2
import scipy.misc
from pfm_lib import load_pfm
import glob

if __name__=='__main__':
	
	#params
	res = 32
	
	# dirs
	seq_path = 'interactive_rectified/'
	#imgs = os.listdir(seq_path)
	imgs = glob.glob(seq_path+'*.pfm')
	
	# pngs dir for video
	pngs_dir = seq_path+'pngs/'
	if not os.path.exists(pngs_dir):
		os.mkdir(pngs_dir)
	
	# load pfm's and save as png frames
	for img in imgs:
		# load
		img_frame = load_pfm(img) # (time_bins, 1024)
		
		# format
		t_bins = img_frame.shape[0]
		frame = img_frame / np.max(img_frame) * 256
		frame = frame.astype('uint8')
		#frame_crop = frame[:,256:768]
		frame_crop = frame
		
		# store png
		path, filename = img.split('\\')
		img_name, ext = filename.split('.')
		scipy.misc.toimage(frame_crop, cmin=np.min(frame), cmax=np.max(frame)).save(pngs_dir+img_name+'.png')	
	
	# format output video
	pngs = os.listdir(pngs_dir)
	width = frame_crop.shape[1]
	height = frame_crop.shape[0]
	fps = 4
	seq_name = 'interactive_rect_video'
	video_name = seq_name + '.avi'
	cap = cv2.VideoCapture(0)
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))
	
	# make video from png's
	print('Rendering Video...')
	for png in pngs:
		img_frame = cv2.imread(pngs_dir+png)
		video.write(img_frame)
	cv2.destroyAllWindows()
	video.release()