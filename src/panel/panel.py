from src.utils import Draggable, Resizable, Size

from typing import TYPE_CHECKING
import sdl2

if TYPE_CHECKING:
    from src.window import Window


class Panel(Draggable, Resizable):
    def __init__(self, title:str, parent_window: Window, size: Size):
        pass
