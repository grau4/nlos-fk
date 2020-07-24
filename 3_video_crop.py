'''
This module reads a video and saves images and a new video from subset of frames of the interactive recording

Author: Javier Grau
'''

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import scipy.misc
from pfm_lib import load_pfm
import glob

if __name__=='__main__':

	#*********************RETRIEVE SUBSET OF FRAMES*********************#
	# params
	t_effective = 32.5 # seconds
	t0 = 29

	# dir for crop video
	crops_dir = 'crop_pngs/'
	if not os.path.exists(crops_dir):
		os.mkdir(crops_dir)
	
	# open video file
	cap= cv2.VideoCapture('video_32.mov')
	n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	fps = int(np.ceil(cap.get(cv2.CAP_PROP_FPS))) # 30fps
	width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	
	# frame crop
	start_fr = t0 * fps
	end_fr = start_fr + t_effective * fps
	i=0
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == False:
			break
		if (i>=start_fr and i<=end_fr):
			i
			cv2.imwrite(crops_dir + str(i).zfill(4)+'.png',frame)
		i+=1
	cap.release()
	cv2.destroyAllWindows()
	
	
	#*********************RENDER CROPPED VIDEO*********************#
	# format output video
	pngs = os.listdir(crops_dir)
	seq_name = 'crop_interactive_video'
	video_name = seq_name + '.avi'
	
	cap2 = cv2.VideoCapture(0)
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))
	
	# make video from png's
	print('Rendering Video...')
	for png in pngs:
		img_frame = cv2.imread(crops_dir+png)
		video.write(img_frame)
	cv2.destroyAllWindows()
	video.release()