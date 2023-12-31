
from __future__ import annotations
import cv2
import numpy as np
from PIL.Image import Image
from typing import Dict, Iterator, Optional, Set, Text, Tuple, Union
import pathlib
from PIL.Image import open as open_image

"""
Template Table:
each table is bined to a Task object



"""
#class TemplateTable:
#    def __init__(self, name: Text, task: Task ) -> None:
#       pass
    
_LOADED_TEMPLATES: Dict[Text, Image] = {}


def _cv_image(img: Image):
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def load(name: Text) -> Image:
    if name not in _LOADED_TEMPLATES:
        #app.log.text("load: %s" % name, level=app.DEBUG)
        img = open_image(pathlib.Path(__file__).parent / "templates_list" / name)
        _LOADED_TEMPLATES[name] = img
    return _LOADED_TEMPLATES[name]


_NOT_EXISTED_NAMES: Set[Text] = set()


def try_load(name: Text) -> Optional[Image]:
    if name in _NOT_EXISTED_NAMES:
        return None
    try:
        return load(name)
    except Exception as ex:
        #app.log.text("can not load: %s: %s" % (name, ex), level=app.DEBUG)
        _NOT_EXISTED_NAMES.add(name)
        return None


def add_middle_ext(name: Text, value: Text) -> Text:
    parts = name.split(".")
    parts.insert(max(len(parts) - 1, 1), value)
    return ".".join(parts)



class Specification:

    @classmethod
    def from_input(cls, input:Input) -> Specification:
        if isinstance(input, Specification):
            return input
        return Specification(input)

    def __init__(self,
                 name: Text,
                 pos: Optional[Text] = None,
                 *,
                 threshold: float = 0.9,
                 lightness_sensitive: bool = True,
                 ) -> None:
        self.name = name
        self.pos = pos
        self.threshold = threshold
        self.lightness_sensitive = lightness_sensitive

    def load_pos(self) -> Optional[Image]:
        return try_load(self.pos or add_middle_ext(self.name, "pos"))

    def match(self, img:Image, pos:Tuple[int,int]) -> bool:
        x, y = pos
        if self.lightness_sensitive:
            #when the template is lightness sensitive, we cut the screenshot image with a specified region
            
            tmpl_img = load(self.name)
            match_img = img.crop((x, y, x + tmpl_img.width, y + tmpl_img.height))

            cv_tmpl_img = np.asarray(tmpl_img.convert("L"))
            cv_match_img = np.asarray(match_img.convert("L"))
            #convert to grayscale
            match_min, match_max, _, _ = cv2.minMaxLoc(cv_match_img)
            tmpl_min, tmpl_max, _, _ = cv2.minMaxLoc(cv_tmpl_img)

            max_diff = (match_max - tmpl_max) / 255.0
            min_diff = (match_min - tmpl_min) / 255.0
            if max_diff < 0:
                max_diff *= -1
                min_diff *= -1

            lightness_similarity = 1 - (abs(max_diff + min_diff) / 2)
            print(
                "lightness match: tmpl=%s, similarity=%.3f"
                % (self, lightness_similarity)
               
            )
            if lightness_similarity < self.threshold:
                print("lightness match: false")
                return False
        print("lightness match: matched")
        return True

        

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return f"tmpl<{self.name}+{self.pos}>" if self.pos else f"tmpl<{self.name}>"


Input = Union[Text,Specification]



def _match_one(
    img: Image, tmpl: Input
) -> Iterator[Tuple[Specification, Tuple[int, int]]]:
    #rp = mathtools.ResizeProxy(TARGET_WIDTH) #initialize a ResizeProxy object
    cv_img = _cv_image(img)#scale the image down by device
    
    tmpl = Specification.from_input(tmpl) #returns a specification

    pos = tmpl.load_pos()
    pil_tmpl = load(tmpl.name) #load the template picture, by load we mean that a png is added to the dictionary
    cv_tmpl = _cv_image(pil_tmpl) # returns a gray scale image
    tmpl_h, tmpl_w = cv_tmpl.shape[:2] 
    if pos:#pos is a grayscale image where only targetted tap point is active
        #if there is pos assigned to this template, which is an image, we conver it to an np array
        cv_pos = np.array(pos.convert("L"))
    else:
        #else we make an empty array of the template width and height
        cv_pos = np.full(cv_img.shape[:2], 255.0, dtype=np.uint8)
    res = cv2.matchTemplate(cv_img, cv_tmpl, cv2.TM_CCOEFF_NORMED) 
   
    #reverse_rp = mathtools.ResizeProxy(app.device.width())
    while True:
        mask = cv_pos[0 : res.shape[0], 0 : res.shape[1]]
        _, max_val, _, max_loc = cv2.minMaxLoc(res, mask=mask) #finding a max location, with in masked region
        x, y = max_loc
        client_pos = x,y#reverse_rp.vector2((x, y), TARGET_WIDTH) #translate the position on pic to the position on client
        if max_val < tmpl.threshold or not tmpl.match(img, client_pos):
            #max val is from a masked region of template matching result, 
            #threshold = 0.9, 
            #the other condition is match() inside specification class
            print(
                "not match: tmpl=%s, pos=%s, similarity=%.3f"
                % (tmpl, max_loc, max_val)
               
            )
            break
        print(
            "match: tmpl=%s, pos=%s, similarity=%.2f" % (tmpl, max_loc, max_val)
        )
        yield (tmpl, client_pos)

        # mark position unavailable to avoid overlap
        cv_pos[max(0, y - tmpl_h) : y + tmpl_h, max(0, x - tmpl_w) : x + tmpl_w] = 0



def match(
    img: Image, *tmpl: Union[Text, Specification]
) -> Iterator[Tuple[Specification, Tuple[int, int]]]:
    match_count = 0
    for i in tmpl:
        for j in _match_one(img, i):
            match_count += 1
            yield j
    if match_count == 0:
        print(f"no match: tmpl={tmpl}")

        