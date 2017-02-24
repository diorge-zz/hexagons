"""
Module coordinate
Axial and cube coordinates for hexagons
"""


class Cube:
    """
    Cube coordinates for a hexagon
    The coordinates (x, y, z) represent an unique hexagon
    """

    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def to_axial(self):
        """ Converts the cube coordinate to an axial coordinate """
        return Axial(self.x, self.z)

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)


class Axial:
    """
    Axial coordinates for a hexagon
    The coordinates (q, r) or (column, row) represent an unique hexagon
    """

    def __init__(self, q, r):
        self._q = q
        self._r = r

    @property
    def q(self):
        return self._q

    @property
    def r(self):
        return self._r

    def __eq__(self, other):
        return (self.q, self.r) == (other.q, other.r)
