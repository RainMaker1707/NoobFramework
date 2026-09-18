from __future__ import annotations
from typing import TYPE_CHECKING

from src.utils import Color

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
        self.width = width
        self.height = height
        self.z_index = z_index
        self.x = x
        self.y = y
        self.panels = None

    def open():
        # TODO: sdl render
        pass
