import cv2
import numpy as np
import tkinter
from tkinter import filedialog, Button


def select_image():
    drawing = False # true if mouse is pressed
    brushsize = [3, 5, 10]
    curBrush = 0
    prev_point = None

    # mouse callback function
    def draw_line(event,x,y,flags,param):
        brushsize = param['brushsize']
        curBrush = param['curBrush']
        prev_point = param['prev_point']

        if event == cv2.EVENT_LBUTTONDOWN:
            param['drawing']=True
            param['prev_point'] = (x,y)

        elif event == cv2.EVENT_MOUSEMOVE:
            if param['drawing'] == True:
                # cv2.circle(mask,(x,y),brushsize[curBrush],(255,255,255,255),-1)
                cv2.line(mask, prev_point, (x,y), (255,255,255,255), brushsize[curBrush])
                param['prev_point'] = (x,y)

        elif event == cv2.EVENT_LBUTTONUP:
            param['drawing'] = False
            # cv2.circle(mask,(x,y),brushsize[curBrush],(255,255,255,255),-1)
            cv2.line(mask, prev_point, (x,y),(255,255,255,255),brushsize[curBrush])
            param['prev_point'] = None


    path = filedialog.askopenfilename()
    if not path:
        return  # no file loaded

    img = cv2.imread(path)
    resized = cv2.resize(img, (128,128), interpolation = cv2.INTER_AREA)
    a = cv2.imwrite("temp_image.png", resized)

    height, width, channel = img.shape
    mask = np.zeros((height, width, channel+1), np.uint8)
    mask[:, :, 0] = img[:, :, 0]
    mask[:, :, 1] = img[:, :, 1]
    mask[:, :, 2] = img[:, :, 2]
    mask[:, :, 3] = np.zeros((height, width))
    w_name = 'Draw on img'
    cv2.namedWindow(w_name)
    param_dict = {'drawing':drawing, 'prev_point':prev_point, 'brushsize':brushsize, 'curBrush':curBrush}

    cv2.setMouseCallback(w_name, draw_line, param=param_dict)
    while cv2.getWindowProperty(w_name, 0) >= 0:
        cv2.imshow(w_name, img)
        cv2.imshow(w_name, mask)
        k = cv2.waitKey(1) & 0xFF
        if k == 32:  # press space to change brush size
            curBrush = (curBrush + 1)%3
            param_dict = {'drawing': drawing, 'prev_point': prev_point, 'brushsize': brushsize, 'curBrush': curBrush}
            cv2.setMouseCallback(w_name, draw_line, param=param_dict)
        elif k == 27:  # press esc to save mask when finished
            mask = mask[:,:,3]
            resized = cv2.resize(mask, (128,128), interpolation = cv2.INTER_AREA)
            cv2.imwrite("temp_mask.png", resized)
            break
        elif k == 8:  # press backspace to reset
            mask = np.zeros((height, width, channel + 1), np.uint8)
            mask[:, :, 0] = img[:, :, 0]
            mask[:, :, 1] = img[:, :, 1]
            mask[:, :, 2] = img[:, :, 2]
            mask[:, :, 3] = np.zeros((height, width))

    cv2.destroyAllWindows()


window = tkinter.Tk()
T = tkinter.Text(window, height=12, width=50)
T.pack()
T.insert(tkinter.END, "\n  Welcome to the inpainting demo tool!\n\n  After loading an image, use mouse to draw.\n\n  "
                      "Press space = change brush size\n\n  Press backspace = reset\n\n  Press ESC = exit and save mask\n\n")
B1 = tkinter.Button(window, text ="Load image and draw mask", command=select_image)
B1.pack()
'''B2 = tkinter.Button(window, text ="Inpaint")
B2.pack()'''

window.mainloop()


'''path = filedialog.askopenfilename()

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

cv2.destroyAllWindows()'''


# os.system("python test.py --checkpoints ./checkpoints/mymodel2 --input ./temp_image.png --mask ./temp_mask.png --output ./test_output/")

# cv2.namedWindow('image')
# output = cv2.imread("./test/output/temp_image")
# cv2.imshow('image', output)
