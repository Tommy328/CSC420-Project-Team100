import os
import shutil
import argparse
import numpy as np
import cv2 

# Classify the mask images by coverage percentage and move the original file to the corresponding folder

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help='path to the dataset')
args = parser.parse_args()

ext = {'.JPG', '.JPEG', '.PNG', '.TIF', 'TIFF'}
total = 3*128*128
images = []
for file in os.listdir(args.path):

    img = cv2.imread(os.path.join(args.path, file))
    
    ratio = (img==255).sum()/total
    if 0.1 <= ratio < 0.2:
        shutil.move(os.path.join(args.path, file), os.path.join('examples/masks/mask10-20', file))
    elif 0.2 <= ratio < 0.3:
        shutil.move(os.path.join(args.path, file), os.path.join('examples/masks/mask20-30', file))
    elif 0.3 <= ratio < 0.4:
        shutil.move(os.path.join(args.path, file), os.path.join('examples/masks/mask30-40', file))
    elif 0.4 <= ratio < 0.5:
        shutil.move(os.path.join(args.path, file), os.path.join('examples/masks/mask40-50', file))
