from screeninfo import Monitor
import sdl2
import ctypes

from src.utils import \
    Singleton, \
    sanitize_width, \
    sanitize_height, \
    Size, \
    ACTIVE_MONITOR, \
    MONITORS, \
    PRIMARY_MONITOR

from src.window import Window


class Application(Singleton):
    def __init__(self, title: str = "NoobFramework", monitor_id: int = 0, width: int = ACTIVE_MONITOR.width, height: int = ACTIVE_MONITOR.height):
        self.title: str = title
        self.size: Size = Size(width, height)
        self.monitor: Monitor = MONITORS[monitor_id] if monitor_id else ACTIVE_MONITOR
        self.main_window: Window = Window(parent_app=self, size=self.size)

    @property
    def width(self) -> int:
        return self.size.width
    
    @width.setter
    def width(self, value: int):
        self.size.width = sanitize_width(value)

    @property
    def height(self) -> int:
        return self.size.height
    
    @height.setter
    def height(self, value: int):
        self.size.height = sanitize_height(value)

    def run(self):
        self.main_window.render()
        event = sdl2.SDL_Event()
        self._is_running = True
        while self._is_running:
            if sdl2.SDL_WaitEvent(ctypes.byref(event)) == 0:
                print(event)
                continue
            
            if event.type == sdl2.SDL_QUIT:
                self.close()
                return
            if event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    self.main_window.resize(event.window.data1, event.window.data2)
                    self.main_window.render()

    def close(self):
        if not self._is_running:
            return
        self.main_window.destroy()
        sdl2.SDL_Quit()
        self._is_running = False