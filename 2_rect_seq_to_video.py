'''
This module reads the pfm files of a sequence and renders a video

Author: Javier Grau
'''

import os
import numpy as np
import cv2
import scipy.misc
from PIL import Image, ImageEnhance
from pfm_lib import load_pfm
import glob

if __name__=='__main__':
	
	#params
	res = 32
	exposure = 7.0
	
	# dirs
	seq_path = 'interactive_rect_Pad/'
	imgs = glob.glob(seq_path+'*.pfm')
	
	# pngs dir for video
	pngs_dir = seq_path+'pngs_enhance/'
	if not os.path.exists(pngs_dir):
		os.mkdir(pngs_dir)
	
	# find maximum pixel value in whole dataset
	max_pix = 0
	for img in imgs:
		img_frame = load_pfm(img)
		max_of_frame = np.max(img_frame)
		
		if max_of_frame>max_pix:
			max_pix = max_of_frame
	
	max_val = max_pix/exposure
	
	
	# load pfm's and save as png frames
	print('Processing frames...')
	for img in imgs:
		# load
		img_frame = load_pfm(img) # (time_bins, 1024)
		
		# xy reshaping
		img_frame = np.reshape(img_frame, (1024, 32, 32))
		img_frame = img_frame.transpose(0,2,1)
		img_frame = np.reshape(img_frame, (1024, 1024))
		
		# format
		t_bins = img_frame.shape[0]
		#frame = img_frame / np.max(img_frame) * 256
		frame = img_frame / max_val * 256
		frame = frame.astype('uint8')
		frame_crop = frame
		
		# store png
		path, filename = img.split('\\')
		img_name, ext = filename.split('.')
		
		pil_img = Image.fromarray(frame)
		enhancer = ImageEnhance.Brightness(pil_img)
		im_out = enhancer.enhance(5)
		im_out.save(pngs_dir+img_name+'.png')
		#scipy.misc.toimage(frame_crop, cmin=0, cmax=max_val).save(pngs_dir+img_name+'.png')	
	
	# format output video
	pngs = os.listdir(pngs_dir)
	width = frame_crop.shape[1]
	height = frame_crop.shape[0]
	fps = 4
	seq_name = 'interactive_rect_'+'exp='+str(exposure)
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