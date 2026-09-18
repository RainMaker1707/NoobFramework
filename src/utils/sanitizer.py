from .monitor import *

def sanitize_width(self, width: int):
    if ACTIVE_MONITOR.width < width:
        width = ACTIVE_MONITOR.width 
    elif width < 0:
        width = 0
    return width

def sanitize_height(self, height: int):
    if ACTIVE_MONITOR.height < height:
        height = ACTIVE_MONITOR.height
    elif height < 0:
        height = 0
    return height