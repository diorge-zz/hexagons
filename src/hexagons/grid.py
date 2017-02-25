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

    def inside_boundary(self, coord):
        """ Checks if a given axial coordinate is inside the grid """
        x, y = coord.q, coord.r
        return abs(x + y) <= self.size

    def hexagon_list(self):
        cn = pointy_corners if self.hex_format == 'pointy' else flat_corners
        for c in self.all_centers():
            yield tuple(cn(c, self.hex_size))

    def all_centers(self):
        wx, wy = (self.window_size / 2, self.window_size / 2)
        topleft_corner = coord.Axial(-self.size, -self.size)
        size = self.hex_size
        c = self.center_hex - topleft_corner
        if self.hex_format == 'flat':
            cx, cy = (size * 3 / 2 * c.q, size * sqrt(3) * (c.r + c.q / 2))
        else:
            cx, cy = (size * sqrt(3) * (c.q + c.r / 2), size * 3 / 2 * c.r)
        dx, dy = wx - cx, wy - cy

        cn = self.center_hex
        pts = [p.to_axial() for p in cn.to_cube().circle_around(self.size)]
        for pt in pts:
            pt = pt - topleft_corner
            if self.hex_format == 'flat':
                yield (size * 3 / 2 * pt.q + dx,
                       size * sqrt(3) * (pt.r + pt.q / 2) + dy)
            else:
                yield (size * sqrt(3) * (pt.q + pt.r / 2) + dx,
                       size * 3 / 2 * pt.r + dy)
