import os
import shutil
import argparse
import numpy as np
import cv2 
import scipy
from scipy.misc import imread
from scipy import ndimage
from PIL import Image

# resize all images in input path to 128x128 and save the resized images in output path

def imsave(img, path):
    im = Image.fromarray(img.cpu().numpy().astype(np.uint8).squeeze())
    im.save(path)

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help='path to the dataset')
parser.add_argument('--output', type=str, help='path to the file list')
args = parser.parse_args()

ext = {'.JPG', '.JPEG', '.PNG', '.TIF', 'TIFF'}

images = []
for file in os.listdir(args.path):

    img = imread(os.path.join(args.path, file))
    img = scipy.misc.imresize(img, [128, 128])
    imsave(img, os.path.join(args.output, file))
    
