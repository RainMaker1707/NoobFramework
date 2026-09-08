from enum import Enum


class Color(tuple, Enum):
    # Neutres & Base
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    CLEAR = (0, 0, 0, 0)

    GRAY_VERY_DARK = (30, 30, 30) 
    GRAY_DARK = (60, 60, 60)
    GRAY = (128, 128, 128)
    GRAY_LIGHT = (200, 200, 200)

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    UI_BG = (35, 39, 46)
    UI_PANEL = (40, 44, 52)
    UI_BORDER = (75, 83, 98)
    PRIMARY = (50, 150, 230)
    SUCCESS = (46, 204, 113)
    WARNING = (241, 196, 15)
    DANGER = (231, 76, 60)

