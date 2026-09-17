from . import Widget
from typing import Any, Callable


class Clickable(Widget):
    def __init__(self, 
            string: str,
            callback: Callable[..., Any],
            position_x: int=0,
            position_y: int=0,
            z_index: int = 0,
            size_x: int=0,
            size_y: int=0,
        ):
        super().__init__(string, x=position_x, y=position_y, w=size_x, h=size_y)
        self.position["z_index"] = z_index
        self._callback = callback


    def clicked(self, *args, **kwargs):
        self._callback(*args, **kwargs)