class Widget:
    def __init__(self, string: str, x: int = 0, y: int = 0, w: int = 0, h: int = 0):
        self.string = string
        self.position = {'x': x, 'y': y}
        self.size = {'x': w, 'y': h}

    def render(self, sdl_renderer, override_x=None, override_y=None, override_w=None, override_h=None):
        raise NotImplementedError("Widget is an abstract class and cannot be renderer. You have to unherit from it and overwritte the render method")
