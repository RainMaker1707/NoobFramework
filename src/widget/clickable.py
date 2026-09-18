from . import Widget
from typing import Any, Callable


class Clickable(Widget):
    def __init__(self, 
            string: str,
            on_click_action: Callable[..., Any],
            position_x: int=0,
            position_y: int=0,
            z_index: int = 0,
            size_x: int=0,
            size_y: int=0,
        ):
        super().__init__(string, x=position_x, y=position_y, w=size_x, h=size_y)
        self.position["z_index"] = z_index
        self._on_click = on_click_action


    def on_click(self, *args, **kwargs):
        self._on_click(*args, **kwargs)

    def is_clicked(self, mouse_pos_x: int, mouse_pos_y: int, override_x: int, override_y: int):
        if not 1920 >= mouse_pos_x >= 0 or not 1080 >= mouse_pos_y >= 0:
            return False
        max_x = self.position['x'] + self.size['x'] + override_x
        max_y = self.position['y'] + self.size['y'] + override_y
        return self.position['x'] <= mouse_pos_x <= max_x and self.position['y'] <= mouse_pos_y <= max_y

    def render(self, sdl_renderer, override_x=None, override_y=None, override_w=None, override_h=None):
        # TODO render button + event on click handling
        pass
