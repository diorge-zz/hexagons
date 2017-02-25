"""
.. module:: grid
    :synopsis: Grids of hexagons and pixel conversions

.. moduleauthor:: Diorge Brognara <diorge.bs@gmail.com>
"""


from math import sqrt, floor, pi, cos, sin
from hexagons.coordinate import Axial


def flat_corners(center, size):
    """Calculates the six corner pixels for flat hexagons

    :param center: central pixel of the hexagon
    :type center: iterable of float (size 2)
    :param size: the size of the hexagon, or half the longest corner
    :type size: float
    :returns: iterable of float -- collection of corners
    """
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = pi / 180 * angle_deg
        x, y = center
        yield (x + size * cos(angle_rad), y + size * sin(angle_rad))


def pointy_corners(center, size):
    """Calculates the six corner pixels for pointy hexagons

    :param center: central pixel of the hexagon
    :type center: iterable of float (size 2)
    :param size: the size of the hexagon, or half the longest corner
    :type size: float
    :returns: iterable of float -- collection of corners
    """
    for i in range(6):
        angle_deg = 60 * i + 30
        angle_rad = pi / 180 * angle_deg
        x, y = center
        yield (x + size * cos(angle_rad), y + size * sin(angle_rad))


class HexagonGrid:
    """Hexagonal grid of hexagonal tiles
    """

    @staticmethod
    def determine_size(window_size, hex_size):
        """Calculates how many hexagons can be fit in the grid

        Similar to each hexagon side, this side is the "radius"
        of the hexagon grid

        :param window_size: pixels in the window square
        :type window_size: float
        :param hex_size: size of the hexagon, in pixels
        :type hex_size: float
        :returns: int -- number of hexagons in the grid radius
        """
        bigger = hex_size * 2
        smaller = (bigger * sqrt(3)) / 2
        total = floor(window_size / smaller)
        if total % 2 == 0:
            return (total - 2) // 2
        else:
            return (total - 1) // 2

    @staticmethod
    def determine_hex_size(window_size, size):
        """Analogous to finding the grid size,
        but in the opposite direction

        :param window_size: pixes in the window square
        :type window_size: float
        :param size: number of hexagons in the grid radius
        :type size: int
        :returns: float -- size of the hexagon, in pixels
        """
        total = size * 2 + 1
        smaller = window_size / total
        bigger = smaller / (sqrt(3) / 2)
        return bigger / 2

    def __init__(self, window_size, hex_size, center_hex, hex_format='pointy'):
        """
        :param window_size: width/height pixels in the window (must be square)
        :type window_size: float
        :param hex_size: size of the hexagons, in pixels
        :type hex_size: float
        :param center_hex: axial coordinate of the center hex
        :type center_hex: Axial
        :param hex_format: either 'flat' or 'pointy'
        :type hex_format: str
        """
        self.window_size = window_size
        self.hex_size = hex_size
        self.hex_format = hex_format
        self.size = HexagonGrid.determine_size(window_size, hex_size)
        self.topleft_corner = Axial(-self.size, -self.size)
        self.move_center(center_hex)

    def move_center(self, new_center):
        self.center_hex = new_center
        wx = wy = self.window_size / 2
        sz = self.hex_size
        c = new_center - self.topleft_corner
        if self.hex_format == 'flat':
            cx, cy = (sz * 3 / 2 * c.q, sz * sqrt(3) * (c.r + c.q / 2))
        else:
            cx, cy = (sz * sqrt(3) * (c.q + c.r / 2), sz * 3 / 2 * c.r)
        self.dx, self.dy = wx - cx, wy - cy

    def inside_boundary(self, coord):
        """Checks if a given axial coordinate is inside the grid

        :param coord: coordinate to be tested against the grid
        :type coord: Axial
        :returns: bool - True if inside, False otherwise
        """
        x, y = coord - self.center_hex
        return (abs(x + y) <= self.size and
                abs(x) <= self.size and
                abs(y) <= self.size)

    def hexagon_list(self):
        """A sequence of hexagons

        Each hexagon is represented by a 6-tuple of points (2-tuples, pixels)
        """
        cn = pointy_corners if self.hex_format == 'pointy' else flat_corners
        for c in self.all_centers():
            yield tuple(cn(c, self.hex_size))

    def all_centers(self):
        """A sequence of hexagon centers

        Each center is represented as a 2-tuple of floats (pixels)
        """
        size = self.hex_size
        cn = self.center_hex
        pts = [p.to_axial() for p in cn.to_cube().circle_around(self.size)]
        for pt in pts:
            pt = pt - self.topleft_corner
            if self.hex_format == 'flat':
                yield (size * 3 / 2 * pt.q + self.dx,
                       size * sqrt(3) * (pt.r + pt.q / 2) + self.dy)
            else:
                yield (size * sqrt(3) * (pt.q + pt.r / 2) + self.dx,
                       size * 3 / 2 * pt.r + self.dy)

    def clicked_hex(self, mousepos):
        """Gets the hexagon clicked

        Calculates which hexagon is in a given window position,
        returns None if no hexagon was clicked

        :param mousepos: point clicked in the window
        :type mousepos: tuple of float
        :returns: Axial or None
        """
        x, y = mousepos
        x = x - self.dx
        y = y - self.dy
        size = self.hex_size
        if self.hex_format == 'flat':
            q = x * (2 / 3) / size
            r = ((-x / 3) + (sqrt(3) / 3) * y) / size
        else:
            q = (x * (sqrt(3) / 3) - (y / 3)) / size
            r = y * ((2 / 3) / size)
        c = Axial(q, r).to_cube().round().to_axial()
        c = c + self.topleft_corner
        if self.inside_boundary(c):
            return c
        else:
            return None
