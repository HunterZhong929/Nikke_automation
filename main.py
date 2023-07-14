import windows_util
import datetime
import win32gui
import win32ui
from pyuac import main_requires_admin

@main_requires_admin
def main():
    window_class = "UnityWndClass"
    window_name = "NIKKE"
    h_wnd = win32gui.FindWindow(window_class,window_name)
    
     
