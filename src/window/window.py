from __future__ import annotations
from typing import TYPE_CHECKING
import sdl2

from src.utils import Color, sanitize_width, sanitize_height, WINDOW_HEADER_SIZE

if TYPE_CHECKING:
    from src.application import Application

class Window:
    def __init__(self,
                parent_app : Application,
                title: str = "NoobFramework's Window",
                width: int = 1920,
                height: int = 1080,
                z_index: int = 0,
                x: int = 0,
                y: int = 0,
                background_color: Color = Color.GRAY_LIGHT,
                resizable: bool = True,
                closable: bool = True
                ):
        self.parent_app = parent_app
        self.title = title
        self.width = sanitize_width(width)
        self.height = sanitize_height(height)
        self.z_index = z_index
        self.x = x
        self.y = y + WINDOW_HEADER_SIZE
        self.panels = None
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
            raise RuntimeError("Failed to initialize SDL2.SDL_INIT_VIDEO")  
        self._sdl_window = sdl2.SDL_CreateWindow(
            self.title.encode('utf-8'),
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            self.width,
            self.height,
            sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_RESIZABLE
        )
        if not self._sdl_window:
            sdl2.SDL_Quit()
            raise RuntimeError("Failed to create window")  
        self._sdl_renderer = sdl2.SDL_CreateRenderer(self._sdl_window, -1, sdl2.SDL_RENDERER_ACCELERATED)


    def resize(self, width:int, height:int):
        self.width = width
        self.height = height
        sdl2.SDL_SetWindowSize(self._sdl_window, self.width, self.height)

    def render(self):
        # Only draw the frame here — never recreate the window/renderer
        sdl2.SDL_SetRenderDrawColor(self._sdl_renderer, 30, 30, 30, 255)
        
        sdl2.SDL_RenderClear(self._sdl_renderer)
        sdl2.SDL_RenderPresent(self._sdl_renderer)

    def destroy(self):
        sdl2.SDL_DestroyRenderer(self._sdl_renderer)
        sdl2.SDL_DestroyWindow(self._sdl_window)

