from screeninfo import Monitor

from src.utils import \
    Singleton, \
    sanitize_width, \
    sanitize_height, \
    ACTIVE_MONITOR, \
    MONITORS, \
    PRIMARY_MONITOR

from src.window import Window


class Application(Singleton):
    def __init__(self, title: str = "NoobFramework", monitor_id: int = 0, width: int = ACTIVE_MONITOR.width, height: int = ACTIVE_MONITOR.height):
        self.title: str = title
        self.width: int = width
        self.height: int = height
        self.monitor: Monitor = MONITORS[monitor_id] if monitor_id else ACTIVE_MONITOR
        self.main_window: Window = Window(parent_app=self, width=self.width, height=self.height)

    @property
    def width(self) -> int:
        return self._width
    
    @width.setter
    def width(self, value: int):
        self._width = sanitize_width(value)

    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, value: int):
        self._height = sanitize_height(value)

    def run(self):
        self.main_window.open()
        # TODO: Event based loop