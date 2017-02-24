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
        if x + y + z != 0:
            raise ValueError('Cube does not slice the x+y+z=0 plane')
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

    def neighbors(self):
        """ The neighbor cubes of the cube, assuming infinite grid """
        return map(lambda d: self + d, Cube._neighbor_directions)

    def diagonals(self):
        """ The coordinates of the six diagonal hexagons """
        return map(lambda d: self + d, Cube._diagonal_directions)

    def __add__(self, other):
        """ Coordinate-wise sum of two cube coordinates """
        return Cube(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __repr__(self):
        return 'Cube({x}, {y}, {z})'.format(x=self.x, y=self.y, z=self.z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

Cube._neighbor_directions = (Cube(1, -1, 0), Cube(1, 0, -1), Cube(0, 1, -1),
                             Cube(-1, 1, 0), Cube(-1, 0, 1), Cube(0, -1, 1))
Cube._diagonal_directions = (Cube(2, -1, -1), Cube(1, 1, -2), Cube(-1, 2, -1),
                             Cube(-2, 1, 1), Cube(-1, -1, 2), Cube(1, -2, 1))


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

    def to_cube(self):
        """ Converts the axial coordinate to a cube coordinate """
        return Cube(self.q, -(self.q + self.r), self.r)

    def neighbors(self):
        """ The neighbor hexagons, assuming infinite grid """
        return(map(lambda d: Axial(self.q + d.q, self.r + d.r),
                   Axial._neighbor_directions))

    def __eq__(self, other):
        return (self.q, self.r) == (other.q, other.r)

    def __repr__(self):
        return 'Axial({q}, {r})'.format(q=self.q, r=self.r)

    def __iter__(self):
        yield self.q
        yield self.r

Axial._neighbor_directions = tuple(map(Cube.to_axial,
                                       Cube._neighbor_directions))
