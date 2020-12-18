import cv2
import numpy as np
import tkinter
from tkinter import filedialog, Button

# In this demo, you can pick an image of your choice and paint a mask on it. Our inpainting model will generate the missing region of the image.

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
                cv2.line(mask, prev_point, (x,y), (255,255,255,255), brushsize[curBrush])
                param['prev_point'] = (x,y)

        elif event == cv2.EVENT_LBUTTONUP:
            param['drawing'] = False
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
                      "Press space = change brush size\n\n  Press backspace = reset\n\n  Press ESC = exit and save mask\n\n  Close this window to start inpainting\n\n")

B1 = tkinter.Button(window, text ="Load image and draw mask", command=select_image)
B1.pack()

window.mainloop()
