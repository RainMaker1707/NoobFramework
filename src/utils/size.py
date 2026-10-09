class Size:
    def __init__(self, height: int, width: int):
        self._height = height
        self._width = width

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        # TODO sanitize value
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        # TODO sanitize value
        self._height = value