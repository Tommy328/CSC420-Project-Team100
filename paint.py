import cv2
import numpy as np
import tkinter
from tkinter import filedialog, Button
import PIL.Image, PIL.ImageTk
import os

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
brushsize = [3, 5, 10]
curBrush = 0
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(mask,(x,y),brushsize[curBrush],(255,255,255,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(mask,(x,y),brushsize[curBrush],(255,255,255,255),-1)

def select_image():
    global path
    path = filedialog.askopenfilename()

window = tkinter.Tk()
path = filedialog.askopenfilename()

img = cv2.imread(path)
resized = cv2.resize(img, (128,128), interpolation = cv2.INTER_AREA)
a = cv2.imwrite("temp_image.png", resized)

height, width, channel = img.shape
mask = np.zeros((height, width, channel+1), np.uint8)
mask[:, :, 0] = img[:, :, 0]
mask[:, :, 1] = img[:, :, 1]
mask[:, :, 2] = img[:, :, 2]
mask[:, :, 3] = np.zeros((height, width))
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
    cv2.imshow('image', img)
    cv2.imshow('image', mask)
    k = cv2.waitKey(1) & 0xFF
    if k == 32:
        curBrush = (curBrush + 1)%3
    elif k == 27:
        mask = mask[:,:,3]
        resized = cv2.resize(mask, (128,128), interpolation = cv2.INTER_AREA)
        cv2.imwrite("temp_mask.png", resized)
        break

cv2.destroyAllWindows()


# os.system("python test.py --checkpoints ./checkpoints/mymodel2 --input ./temp_image.png --mask ./temp_mask.png --output ./test_output/")

# cv2.namedWindow('image')
# output = cv2.imread("./test/output/temp_image")
# cv2.imshow('image', output)
