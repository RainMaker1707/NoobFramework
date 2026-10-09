class Position:
    def __init__(self, x: int, y: int, z_index: int):
        self._x = x
        self._y = y
        self._z_index = z_index

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        # TODO sanitize
        self._x = value

    @property
    def y(self):
        return self._y

    @x.setter
    def y(self, value: int):
        # TODO sanitize
        self._y = value

    @property
    def z_index(self):
        return self._z_index

    @x.setter
    def z_index(self, value: int):
        # TODO sanitize
        self._z_index = value