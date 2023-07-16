

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
import device


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
    out_img = np.zeros((720, 1080), dtype=np.uint8)
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
    
    device.g.last_screenshot_save_path = "last_screenshot.png"
    
    hwnd_target =  win32gui.FindWindow("UnityWndClass","NIKKE")
    
    client = device.Device(hwnd_target)

    screenshot = client.screenshot()
    screenshot.save("last_screenshot.png")


        
        
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

    