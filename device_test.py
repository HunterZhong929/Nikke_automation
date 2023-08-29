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
    matome_defense_post(client) #make cross button template after tap reward
    
    get_defense_post(client)
    get_daily_paid_shop(client) #some times the click is too quick
    #
    #
    get_friend_point(client)
    daily_friend_point_gacha(client)
    get_daily_hakken(client)
    get_daily_free_shop(client)
def matome_defense_post(client:device.Device):
    import action
    once = True
    while once:
        tmpl, pos = action.wait_image("defense_post_button.png",
                                        "matome_destroy_processing.png",
                                        "matome_destroy.png",
                                      "tap_get_reward.png",
                                      "tap_get_reward_text.png"
                                        #"on_commander_level_up.png",
                                          )
    
        name = tmpl.name
        print(name)
        print(pos)
        if name == "tap_get_reward.png" or name == "tap_get_reward_text.png":
            
            client.tap(action.template_rect(tmpl,pos))
            #TODO 
            #need a tap point that's outside of the box
            x1,x2,_,_ = action.template_rect(tmpl,pos)
            w = 0+x1-200
            h = x2 - 200
            side_rect = (0,0,w,h)
            client.tap(side_rect)
            once = False
        else:
            client.tap(action.template_rect(tmpl,pos))

def get_defense_post(client:device.Device):

    import action
    once = True
    while once:
        tmpl, pos = action.wait_image("defense_post_button.png",
                                    "get_defense_reward.png",
                                      "tap_get_reward.png",
                                      "tap_get_reward_text.png", 
                                        "on_commander_level_up.png"
                                          )
    
        name = tmpl.name
        print(name)
        print(pos)
        if name == "tap_get_reward.png":
            
            client.tap(action.template_rect(tmpl,pos))
            once = False
        else:
            client.tap(action.template_rect(tmpl,pos))

def get_daily_paid_shop(client:device.Device):
    
    import action
    once = True
    while once:
        tmpl, pos = action.wait_image("paid_shop.png",
                                    "daily_paid_shop_icon.png",
                                      "daily_free_pack.png",
                                      "daily_gift.png",
                                      "tap_get_reward.png",
                                      "pop_up_paid_shop.png"
                                          )
    
        name = tmpl.name
        print(name)
        print(pos)
        if name == "tap_get_reward.png":
            
            client.tap(action.template_rect(tmpl,pos))
            action.wait_tap_image("home_button.png")
            once = False
        else:
            client.tap(action.template_rect(tmpl,pos))

def get_daily_free_shop(client:device.Device):
    
    import action
    once = True
    while once:
        tmpl, pos = action.wait_image("free_shop.png",
                                    "buy_free_item.png",
                                    "free_shop_sale_item.png",
                                      "tap_get_reward.png",
                                      
                                          )
    
        name = tmpl.name
        print(name)
        print(pos)
        if name == "tap_get_reward.png":
            
            client.tap(action.template_rect(tmpl,pos))
            action.wait_tap_image("home_button.png")
            once = False
        else:
            client.tap(action.template_rect(tmpl,pos))

def daily_friend_point_gacha(client:device.Device):
    import action
    action.wait_tap_image("member_gacha.png")
    action.wait_tap_image("gacha_left_arrow.png")
    action.wait_tap_image("friend_point_gacha_once.png")
    action.wait_tap_image("gacha_skip.png")
    action.wait_tap_image("gacha_ok.png")
    action.wait_tap_image("lobby.png")
def get_friend_point(client:device.Device):
    import action
    once = True
    while once:
        tmpl, pos = action.wait_image("friend_list_button.png",
                                    "send_friend_point.png",
                                    "OK_button.png"
                                      
                                          )
    
        name = tmpl.name
        print(name)
        print(pos)
        #TODO some minor pop up window not made template yet
        if name == "send_friend_point.png":
            
            client.tap(action.template_rect(tmpl,pos))
            action.wait_tap_image("blue_cross_out2.png")
            action.wait_tap_image("blue_cross_out.png")
            once = False
        else:
            client.tap(action.template_rect(tmpl,pos))

def get_daily_hakken(client:device.Device):
    
    pass
    import action
    once = True
    while once:
        tmpl, pos = action.wait_image("front_line_base.png",
                                    "hakken_button.png",
                                      "hakken_get_reward.png",
                                      "hakken_all_button.png",
                                      "hakken_dispatch.png",
                                      "tap_get_reward.png"
                                          )
    
        name = tmpl.name
        print(name)
        print(pos)
        if name == "hakken_dispatch.png":
            
            client.tap(action.template_rect(tmpl,pos))
            action.wait_tap_image("cross_out.png")
            action.wait_tap_image("home_button.png")
            once = False
        else:
            client.tap(action.template_rect(tmpl,pos))





if __name__ == "__main__":
    main()

