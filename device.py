
from __future__ import annotations
import util 
import datetime as dt
from PIL.Image import Image
import win32gui
from random import randint
from typing import Tuple

Rect = Tuple[int, int, int, int]
    
class g:
    
    last_screenshot_save_path: str = ""

def _random_point(rect: Rect) -> Tuple[int, int]:
    x, y, w, h = rect
    return (randint(x, x + w), randint(y, y + h))




class Device():
    def __init__(self, client: int) -> None:
        self._c = client #this is the window handle
        self._cached_screenshot = (dt.datetime.fromtimestamp(0), Image())
        self.dc = window_dc = win32gui.GetWindowDC(client)
        left, top, right, bot = win32gui.GetWindowRect(client)
        self.w = right - left
        self.h = bot - top
        self.setup()
    
    def height(self) -> int:
        return self.h
    
    def width(self) -> int:
        return self.w

    def invalidate_screenshot(self):
        self._cached_screenshot = (dt.datetime.fromtimestamp(0), Image())

    def screenshot(self, *, max_age: float = 1) -> Image:
        
        
        cached_time, _ = self._cached_screenshot
        if cached_time < dt.datetime.now() - dt.timedelta(seconds=max_age):
            new_img = util.screenshot_pil_crop(self._c).convert("RGB")
            if g.last_screenshot_save_path!="":
                new_img.save(g.last_screenshot_save_path, format="PNG")
            print("screenshot")
            #app.log.text("screenshot", level=app.DEBUG)
            self._cached_screenshot = (dt.datetime.now(), new_img)
        return self._cached_screenshot[1]


    def setup(self) ->None:
        util.set_client_size(self._c,1080,720)
        
    def tap(self, area: Rect) -> None:
        

        print("tap(%s)" % (area,))
        util.click_at(self._c,_random_point(area))
        self.invalidate_screenshot()

    def swipe(self, start: Rect, end: Rect, *, duration: float = 0.1) -> None:
        

        print(
            "swipe(%s, %s, duration=%s)" % (start, end, duration)
        )
        p1 = _random_point(start)
        p2 = _random_point(end)
        util.drag_at(self._c,p1, dx=p2[0] - p1[0], dy=p2[1] - p1[1], duration=duration)
        self.invalidate_screenshot()
