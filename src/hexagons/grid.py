"""
Module grid
Grids for hexagons
"""


from math import sqrt, floor, pi, cos, sin
import coordinate as coord


def flat_corners(center, size):
    """
    Return the six corners from a center point, for flat hexagons
    """
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = pi / 180 * angle_deg
        x, y = center
        yield (x + size * cos(angle_rad), y + size * sin(angle_rad))


def pointy_corners(center, size):
    """
    Return the six corners from a center point, for pointy hexagons
    """
    for i in range(6):
        angle_deg = 60 * i + 30
        angle_rad = pi / 180 * angle_deg
        x, y = center
        yield (x + size * cos(angle_rad), y + size * sin(angle_rad))


class HexagonGrid:
    """
    Hexagonal grid of hexagonal tiles
    """

    def __init__(self, window_size, hex_size, center_hex, hex_format='pointy'):
        """
        :param window_size: width/height pixels in the window (must be square)
        :param hex_size: size of the hexagons, in pixels
        :param center_hex: axial coordinate of the center hex
        :param hex_format: either 'flat' or 'pointy'
        """
        self.window_size = window_size
        self.hex_size = hex_size
        self.center_hex = center_hex
        self.hex_format = hex_format

        if hex_format == 'flat':
            self.hex_width = hex_size * 2
            self.hex_height = (self.hex_width * sqrt(3)) / 2
            self.size = floor(self.window_size / self.hex_height)
            if self.size % 2 == 0:
                self.size = (self.size - 2) // 2
            else:
                self.size = (self.size - 1) // 2
        elif hex_format == 'pointy':
            self.hex_height = hex_size * 2
            self.hex_width = (self.hex_height * sqrt(3)) / 2
            self.size = floor(self.window_size / self.hex_width)
            if self.size % 2 == 0:
                self.size = (self.size - 2) // 2
            else:
                self.size = (self.size - 1) // 2
        else:
            raise ValueError('Unknown hex_format: ' + hex_format)

        wx = wy = window_size / 2
        self.topleft_corner = coord.Axial(-self.size, -self.size)
        sz = self.hex_size
        c = center_hex - self.topleft_corner
        if self.hex_format == 'flat':
            cx, cy = (sz * 3 / 2 * c.q, sz * sqrt(3) * (c.r + c.q / 2))
        else:
            cx, cy = (sz * sqrt(3) * (c.q + c.r / 2), sz * 3 / 2 * c.r)
        self.dx, self.dy = wx - cx, wy - cy

    def inside_boundary(self, coord):
        """ Checks if a given axial coordinate is inside the grid """
        x, y = coord.q, coord.r
        return (abs(x + y) <= self.size and
                abs(x) <= self.size and
                abs(y) <= self.size)

    def hexagon_list(self):
        """
        A sequence of tuples, each representing the six corners of a hexagon,
        in pixels
        """
        cn = pointy_corners if self.hex_format == 'pointy' else flat_corners
        for c in self.all_centers():
            yield tuple(cn(c, self.hex_size))

    def all_centers(self):
        """
        The center of every hexagon in the grid, in pixels
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
        """
        Gets the axial coordinate of a click
        Returns None if no hex was clicked
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
        c = coord.Axial(q, r).to_cube().round().to_axial()
        c = c + self.topleft_corner
        if self.inside_boundary(c):
            return c
        else:
            return None
