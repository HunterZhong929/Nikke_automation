import template
import device
import PIL.Image
import win32gui
import numpy as np
from pyuac import main_requires_admin

@main_requires_admin
def main():
    device.g.last_screenshot_save_path = "last_screenshot.png"
    
    hwnd_target =  win32gui.FindWindow("UnityWndClass","NIKKE")
    
    client = device.Device(hwnd_target)

    screenshot = client.screenshot()
    
    import config
    config.config.WINDOW_HANDLE = hwnd_target

    import action

    #client.tap((100,200,300,200))

    #next(iter)
    once = True
    while once:
        tmpl, pos = action.wait_image("defense_post_button.png",
                                    "get_defense_reward.png",
                                      "tap_get_reward.png",
                                          )
    
        name = tmpl.name
        print(name)
        print(pos)
        if name == "tap_get_reward.png":
            client.tap((100,100,100,100))
            client.tap(action.template_rect(tmpl,pos))
            once = False
        else:
            client.tap(action.template_rect(tmpl,pos))



if __name__ == "__main__":
    main()

