'''
Created on Dec 16, 2018

@author: jgraucho
'''
import numpy as np
import re
import sys


def load_pfm(file_name):
    '''
    Load a PFM file into a Numpy array. Note that it will have
    a shape of H x W, not W x H. Returns a tuple containing the
    loaded image and the scale factor from the file.
    '''
    color = None
    width = None
    height = None
    scale = None
    endian = None
    
    file = open(file_name, 'rb')
    #header = file.readline().rstrip()
    header = file.readline().decode("utf-8").rstrip()
    if header == 'PF':
        color = True    
    elif header == 'Pf':
        color = False
    else:
        raise Exception('Not a PFM file.')
    
    dim_match = re.match(r'^(\d+)\s(\d+)\s$', file.readline().decode("utf-8"))
    if dim_match:
        width, height = map(int, dim_match.groups())
    else:
        raise Exception('Malformed PFM header.')
    
    scale = float(file.readline().decode("utf-8").rstrip())
    if scale < 0: # little-endian
        endian = '<'
        scale = -scale
    else:
        endian = '>' # big-endian
    
    data = np.fromfile(file, endian + 'f')
    shape = (height, width, 3) if color else (height, width)
    file.close()
    return np.reshape(data, shape)

def save_pfm(filename, image, scale = 1):
    '''
    Save a Numpy array to a PFM file.
    '''
    color = None    
    file = open(filename, 'wb')
    if image.dtype.name != 'float32':
        raise Exception('Image dtype must be float32.')
    
    if len(image.shape) == 3 and image.shape[2] == 3: # color image
        color = True
    elif len(image.shape) == 2 or len(image.shape) == 3 and image.shape[2] == 1: # greyscale
        color = False
    else:
        raise Exception('Image must have H x W x 3, H x W x 1 or H x W dimensions.')
    
    
    file.write(b'PF\n' if color else b'Pf\n')
    file.write(b'%d %d\n' % (image.shape[1], image.shape[0]))
    
    endian = image.dtype.byteorder
    
    if endian == '<' or endian == '=' and sys.byteorder == 'little':
        scale = -scale
    
    file.write(b'%f\n' % scale)
    
    image.tofile(file)
    file.close() 