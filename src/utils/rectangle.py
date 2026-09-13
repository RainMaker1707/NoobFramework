import sdl2


class Moveable:

    def __init__(self, x: int=0, y: int=0, z_index: int=0):
        self.x: int = x
        self.y: int = y
        self.z_index: int = z_index

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        if value < 0:
            raise ValueError("Position X cannot be lower than 0")
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        if value < 0:
            raise ValueError("Position Y cannot be lower than 0")
        self._y = value

    @property
    def z_index(self):
        return self._z

    @z_index.setter
    def z_index(self, value: int):
        self._z = value

    def move(self, x: int, y: int):
        self.x = x
        self.y = y

    def translate_x(self, distance: int):
        self.x += distance

    def translate_y(self, distance: int):
        self.y += distance

    def move_back(self, amount: int = 1):
        self.z_index -= amount

    def move_front(self, amount: int = 1):
        self.z_index += amount


class Resizeable:
    def __init__(self, x: int=0, y: int=0):
        self.width: int = x
        self.height: int = y

    @property
    def width(self):
        return self._w

    @width.setter
    def width(self, value: int):
        if value < 0:
            raise ValueError("Size X cannot be lower than 0")
        self._w = value

    @property
    def height(self):
        return self._h

    @height.setter
    def height(self, value: int):
        if value < 0:
            raise ValueError("Size Y cannot be lower than 0")
        self._h = value

    def resize(self, width: int, height: int):
        self.width = width
        self.height = height

    def resize_ratio(self, width: int = None, height: int = None):
        if width is None and height is None:
            raise ValueError("Specify either width or height, but not both")

        if width is not None:
            if self.width <= 0:
                raise ValueError("Cannot preserve aspect ratio with a zero or a negative width")
            height = round(width * self.height / self.width)
        else:
            if self.height <= 0:
                raise ValueError("Cannot preserve aspect ratio with a zero or a negative height")
            width = round(height * self.width / self.height)

        self.resize(width, height)


class Draggable:
    def __init__(self):
        self.start_position: tuple[int, int] | None = None
        self.current_position: tuple[int, int] | None = None
        self.state: str = "idle"

    def start_drag(self, x: int, y: int):
        position = (x, y)
        self.start_position = position
        self.current_position = position
        self.state = "dragging"

    def drag_to(self, x: int, y: int):
        if self.state != "dragging":
            raise RuntimeError("Cannot drag before starting a drag")
        self.current_position = (x, y)

    def stop_drag(self):
        self.state = "idle"

    def reset_drag(self):
        self.start_position = None
        self.current_position = None
        self.state = "idle"

class Rectangle(Moveable, Resizeable):
    def __init__(self, x = 0, y = 0, z = 0, width=0, height=0):
        Moveable.__init__(self, x, y, z)
        Resizeable.__init__(self, width, height)

    @property
    def top(self):
        return min(self.y, self.y + self.height)

    @property
    def right(self):
        return max(self.x, self.x + self.width)

    @property
    def bottom(self):
        return max(self.y, self.y + self.height)

    @property
    def left(self):
        return min(self.x, self.x + self.width)

    @property
    def sdl(self):
        return sdl2.SDL_Rect(
            int(self.x),
            int(self.y),
            int(self.width),
            int(self.height)
        )
