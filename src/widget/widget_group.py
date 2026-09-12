from . import Widget
from src import allow_batch, Color
from ctypes import byref
from enum import Enum
import sdl2

class Orientation(Enum):
    HORIZONTAL=0,
    VERTICAL=1,


class WidgetGroup(Widget):
    def __init__(self, group_name: str, x: int = 0, y: int = 0, w: int = 0, h: int = 0, orientation: Orientation = Orientation.VERTICAL, widget_list: list[Widget] = []):
        super().__init__(group_name, x, y, w, h)
        self.orientation: Orientation = orientation
        self.widgets: dict[str, Widget]= {}
        self.add_widget(widget_list)

    def render(self, sdl_renderer, override_x=None, override_y=None, override_w=None, override_h=None):
        base_x = override_x if override_x is not None else self.rectangle.x
        base_y = override_y if override_y is not None else self.rectangle.y
        base_w = override_w if override_w is not None else self.rectangle.width
        base_h = override_h if override_h is not None else self.rectangle.height

        if base_w > 0 and base_h > 0:
            border_color = Color.GRAY_LIGHT
            sdl2.SDL_SetRenderDrawColor(sdl_renderer, border_color[0], border_color[1], border_color[2], 180)
            rect = sdl2.SDL_Rect(int(base_x), int(base_y), int(base_w), int(base_h))
            sdl2.SDL_RenderDrawRect(sdl_renderer, byref(rect))
        for key in self.widgets.keys():
            # TODO: implement layout logic
            self.widgets.get(key).render(sdl_renderer, override_x=override_x, override_y=override_y, override_w=override_w, override_h=override_h)

    @allow_batch
    def add_widget(self, o_widget: Widget, string: str = ""):
        if not string:
            string = o_widget.string()
        if self.widgets.get(string) is not None:
            raise ValueError(f"Widget {string} already present in group {self.string}")
        self.widgets[string] = o_widget
