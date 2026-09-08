from src import Color, Menu, Button, allow_batch, Widget, WidgetGroup
import sdl2
import ctypes
import sdl2.sdlttf as sdlttf
from copy import deepcopy

sdlttf.TTF_Init()


class Panel():
    def __init__(
        self,
        string: str,
        size_x: int = 1080, 
        size_y: int = 1920, 
        position_x: int = 0, 
        position_y: int = 0, 
        z_index: int = 0,
        color: Color = Color.BLUE,
        border_color: Color = Color.GRAY_LIGHT,
        can_accept_drop: bool = False,
        menu: Menu|None = None,
        ):
        self.string: str = string
        self.position: dict[str, int] = {'x': position_x, 'y': position_y, 'z': z_index}
        self.size: dict[str, int] = {'x': size_x, 'y': size_y}
        self.color: Color = color
        self.border_color: Color = border_color
        self.header_height: int = 25
        self.can_accept_drop: bool = can_accept_drop
        self.menu: Menu|None = menu
        self._font = sdlttf.TTF_OpenFont(b"C:\\Windows\\Fonts\\arial.ttf", 14)
        self._font_color = Color.WHITE
        self.groups: list[WidgetGroup] = []
        self.default_group: WidgetGroup = WidgetGroup(f"{self.string}_root_group")
        self.groups.append(self.default_group)

    @property
    def z_index(self):
        return self.position['z']
    
    @z_index.setter
    def z_index(self, value: int):
        self.position['z'] = value

    @property
    def position_x(self):
        return self.position['x']

    @position_x.setter
    def position_x(self, value: int):
        if value < 0: 
            raise ValueError("Position X cannot be lower than 0")
        self.position_x = value
    
    @property
    def position_y(self):
        return self.position['y']
    
    @position_y.setter
    def position_y(self, value: int):
        if value < 0: 
            raise ValueError("Position Y cannot be lower than 0")
        self.position_y = value

    def render(self, sdl_renderer):
        rect = sdl2.SDL_Rect(
                int(self.position['x']),
                int(self.position['y']),
                int(self.size['x']),
                int(self.size['y'])
            )
        # Background color
        r, g, b = getattr(self, 'color', Color.BLUE)
        sdl2.SDL_SetRenderDrawColor(sdl_renderer, r, g, b, 255)
        sdl2.SDL_RenderFillRect(sdl_renderer, ctypes.byref(rect))
        if self.header_height > 0:
            rect_header = sdl2.SDL_Rect(
                int(self.position['x']),
                int(self.position['y']),
                int(self.size['x']),
                int(self.header_height)
            )
            br, bg, bb = self.border_color[:3]
            sdl2.SDL_SetRenderDrawColor(sdl_renderer, br, bg, bb, 255)
            sdl2.SDL_RenderFillRect(sdl_renderer, ctypes.byref(rect_header))
            if self.string and self._font:
                text_color = sdl2.SDL_Color(self._font_color[0], self._font_color[1], self._font_color[2], 255)
                text_surface = sdlttf.TTF_RenderUTF8_Blended(
                    self._font, 
                    self.string.encode('utf-8'), 
                    text_color
                )
                if text_surface:
                    text_texture = sdl2.SDL_CreateTextureFromSurface(sdl_renderer, text_surface)
                    # Alignement du texte (marge de 5px à gauche, centré en hauteur dans le header)
                    text_w = text_surface.contents.w
                    text_h = text_surface.contents.h
                    dst_rect = sdl2.SDL_Rect(
                        int(self.position['x'] + 5),
                        int(self.position['y'] + (self.header_height - text_h) // 2),
                        text_w,
                        text_h
                    )
                    sdl2.SDL_RenderCopy(sdl_renderer, text_texture, None, ctypes.byref(dst_rect))
                    sdl2.SDL_FreeSurface(text_surface)
                    sdl2.SDL_DestroyTexture(text_texture)
        previous_groups_height = self.header_height
        for group in self.groups:
            group.render(sdl_renderer, override_x=self.position_x, override_y=self.position_y+previous_groups_height)
            previous_groups_height += group.size['y']

    def is_header_clicked(self, x: int, y: int) -> bool:
        return (
            self.position['x'] <= x <= self.position['x'] + self.size['x'] and
            self.position['y'] <= y <= self.position['y'] + self.header_height
        )

    def is_point_inside(self, x: int, y: int) -> bool:
        return (
            self.position['x'] <= x <= self.position['x'] + self.size['x'] and
            self.position['y'] <= y <= self.position['y'] + self.size['y']
        )

    @allow_batch
    def add(self, widget: Widget):
        if isinstance(widget, WidgetGroup):
            self.groups.append(widget)
        elif isinstance(widget, Widget):
            self.default_group.append(widget)
        else:
            raise ValueError(f"Cannot append type {type(widget)} to Panel, only Widget and derivated are authorized")
