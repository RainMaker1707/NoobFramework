from src import Color
from . import Widget, Clickable
import sdl2
import ctypes
import sdl2.sdlttf as sdlttf

sdlttf.TTF_Init()

class Button(Clickable):
    def __init__(self, 
            string: str,
            callback: func,
            position_x: int=0,
            position_y: int=0,
            z_index: int = 0,
            size_x: int=0,
            size_y: int=0,
        ):
        super().__init__(x=position_x, y=position_y, w=size_x, h=size_y)
        self.string = string
        self.callback = callback
        self.active = True
        self._font = sdlttf.TTF_OpenFont(b"src/fonts/arial.ttf", 14)
        self._font_color = Color.WHITE
        self.margin = {"x": 15, "y": 10}
        self.padding = {"x": 10, "y": 5}

    def render(self, sdl_renderer, override_x=None, override_y=None, override_w=None, override_h=None):
        x = override_x if override_x is not None else self.position['x']
        y = override_y if override_y is not None else self.position['y']
        w = override_w if override_w is not None else self.size['x']
        h = override_h if override_h is not None else self.size['y']
        rect = sdl2.SDL_Rect(x, y, w, h)
        # Background color
        r, g, b = getattr(self, 'color', Color.GRAY_DARK)
        sdl2.SDL_SetRenderDrawColor(sdl_renderer, r, g, b, 255)
        sdl2.SDL_RenderFillRect(sdl_renderer, ctypes.byref(rect))
        if self.string and self._font:
            text_color = sdl2.SDL_Color(self._font_color[0], self._font_color[1], self._font_color[2], 255)
            text_surface = sdlttf.TTF_RenderUTF8_Blended(
                self._font, 
                self.string.encode('utf-8'), 
                text_color
            )
            if text_surface:
                text_texture = sdl2.SDL_CreateTextureFromSurface(sdl_renderer, text_surface)
                dst_rect = sdl2.SDL_Rect(
                    int(x + self.margin["x"] + self.padding["x"]),
                    int(y + self.margin["y"] + self.padding["y"]),
                    text_surface.contents.w,
                    text_surface.contents.h
                )
                sdl2.SDL_RenderCopy(sdl_renderer, text_texture, None, ctypes.byref(dst_rect))
                sdl2.SDL_FreeSurface(text_surface)
                sdl2.SDL_DestroyTexture(text_texture)
        

    def toggle_active(self):
        self.active = not self.active
    
    def clicked(self):
        if not self.active:
            return
        self.callback()
