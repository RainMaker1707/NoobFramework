from screeninfo import Monitor
import sdl2
import ctypes

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
        self.main_window.render()
        # TODO: Event based loop
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
        self._is_running = False
        self.main_window.destroy()
        sdl2.SDL_Quit()