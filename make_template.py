

import win32con
import win32gui
import win32ui
import time
import PIL.Image
from typing import Text
import cv2
import numpy as np
import argparse
import sys
import os
from pyuac import main_requires_admin
import util


def add_middle_ext(name: Text, value: Text) -> Text:
    parts = name.split(".")
    parts.insert(max(len(parts) - 1, 1), value)
    return ".".join(parts)


def match(image:PIL.Image.Image, template:PIL.Image.Image,threshold:float):
    
    #both input image should already be in grayscale
    image_np = np.array(image.convert('L'))
    template_np = np.array(template.convert('L'))
    result = cv2.matchTemplate(image_np,template_np,cv2.TM_CCOEFF_NORMED)
    _ , max_val, _, _ = cv2.minMaxLoc(result)
    print("match% = ", max_val)
    locations = np.where(result >= threshold)
    return locations 


def create_pos_mask(
    template_img: PIL.Image.Image, #the button or templates you want to find in the whole picture
    game_img: PIL.Image.Image,#this is the base image, the whole picture
    threshold: float,
    padding: int,
):
    #app.device = ImageDeviceService(game_img)
    #pos_name = add_middle_ext(name, "pos")
    origin_img = np.array(game_img.convert('L'))
    ow,oh = origin_img.shape[:2]
    print(ow,oh)
    #the below weird number is for padding of the client size and the top window bar when we taking a screen shot, there are 8 extra pixel on left, right and bottom, 31 for the top bar
    out_img = np.zeros((720+31+8, 1080+16), dtype=np.uint8)
    locations = match(game_img,template_img,threshold)
    mask = np.zeros(np.array(game_img.convert('L')).shape[:2], np.uint8)
    template_h, template_w = np.array(template_img.convert('L')).shape[:2]
    for pt in zip(*locations[::-1]):
        if mask[pt[1] + int(round(template_h/2)), pt[0] + int(round(template_w/2))] != 255:
            mask[pt[1]:pt[1]+template_h, pt[0]:pt[0]+template_w] = 255
            top_left = pt
            bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
            x,y = pt
            print(pt)
            out_img[y - padding : y + padding, x - padding : x + padding] = 255
            cv2.rectangle(origin_img, top_left, bottom_right, 255, 2)
    
    
    cv2.imshow("origin",origin_img)
    cv2.imshow("out", out_img)
    cv2.waitKey()
    cv2.destroyWindow("out")
    return PIL.Image.fromarray(out_img).convert("1") #converts to black and white
    




@main_requires_admin
def main():
    path = r"C:\Hunter\Nikke_Automation\templates_list"        

    parser = argparse.ArgumentParser(description='provide a template image, make template pos ')

    parser.add_argument('--name', help='template name')
    args = parser.parse_args()
    template_name = "\\"+args.name+".png"
    print(template_name)
    
    #test: screenshot
    hwnd_target =  win32gui.FindWindow("UnityWndClass","NIKKE")
    win32gui.ShowWindow(hwnd_target,5)
    win32gui.SetForegroundWindow(hwnd_target) #Chrome handle be used for test 
    set_window_size(hwnd_target)
    print(hwnd_target)
    print("set size succesful")
    left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
    w = right - left
    h = bot - top
    
    
    time.sleep(1.0)

    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = PIL.Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)

    if result == None:
        #PrintWindow Succeeded
        print("success")
        im.save("last_screenshot.png")
        
    template_pil = PIL.Image.open(path+template_name)
    image_pil = PIL.Image.open("last_screenshot.png")
    locations = match(image_pil,template_pil,0.9)
    res = create_pos_mask(template_pil,image_pil,0.9,2)
    print(locations)

    print("Is the result correct? (y/n)")
    ans = str(input())
    if ans == 'y' or ans == 'Y':
        res.save(path+add_middle_ext(template_name,"pos"))
    

    
   



def set_window_size(hwnd:int):
    util.set_client_size(hwnd, 1080, 720)
    
if __name__ == "__main__":
    main()


"""
1.find the window


2.read the context
3.do the assigned task
4.


"""

    