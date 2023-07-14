import cv2
import numpy as np
from PIL.Image import Image
from typing import Optional, Iterator, Set, Text, Tuple, Union


"""
Template Table:
each table is bined to a Task object



"""
class TemplateTable:
    def __init__(self, name: Text, task: Task ) -> None:
        pass
        



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
                 threshold: float = 0.8,
                 ) -> None:
        self.name = name
        self.pos = pos
        self.threshold = threshold


    def load_pos(self) -> Optional[Image]:
        pass

    def match(self, img:Image, pos:Tuple[int,int]) -> bool:
        x,y = pos

        tmpl_img = load(self.name)
        match_img = 

        cv_tmpl_img = np.asarray(tmpl_img.convert("L"))
        cv_match_img = np.asarray(match_img.convert("L"))

        pass

    def __repr__(self):
        pass

    def __str__(self) -> str:
        pass




Input = Union[Text,Specification]


