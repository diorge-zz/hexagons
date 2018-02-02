"""
.. module:: grid
    :synopsis: Grids of hexagons and pixel conversions

.. moduleauthor:: Diorge Brognara <diorge.bs@gmail.com>
"""


from collections import namedtuple
from math import sqrt, floor, pi, cos, sin
from hexagons.coordinate import Axial


Hex = namedtuple('Hex', ['axiscoord', 'pixelcenter', 'pixelcorners'])


class HexagonGrid:
    """Hexagonal grid of hexagonal tiles

    Note the grid itself will be the opposite of the hexes --
    if the hexes are pointy, the hexagon-grid is flat, and vice-versa.
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

    @staticmethod
    def _flat_corners(center, size):
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
            centerx, centery = center
            yield (centerx + size * cos(angle_rad),
                   centery + size * sin(angle_rad))

    @staticmethod
    def _pointy_corners(center, size):
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
            centerx, centery = center
            yield (centerx + size * cos(angle_rad),
                   centery + size * sin(angle_rad))

    def __init__(self, window_size, center_hex, hex_format='pointy',
                 grid_size=0, hex_size=0):
        """Creates a new hexagonal grid

        Prefers to use grid_size instead of hex_size if that variable is set.
        One of these two variables must be set.

        :param window_size: width/height pixels in the window (must be square)
        :type window_size: float
        :param center_hex: axial coordinate of the center hex
        :type center_hex: Axial
        :param hex_format: either 'flat' or 'pointy'
        :type hex_format: str
        :param grid_size: size of the grid, in hexagons
        :type grid_size: int
        :param hex_size: size of the hexagons, in pixels
        :type hex_size: float
        """
        if grid_size > 0:
            self.size = grid_size
            self.hex_size = HexagonGrid.determine_hex_size(window_size, grid_size)
        else:
            self.hex_size = hex_size
            self.size = HexagonGrid.determine_size(window_size, hex_size)
        self.window_size = window_size
        self.hex_format = hex_format
        self.topleft_corner = Axial(-self.size, -self.size)
        self.move_center(center_hex)

    def move_center(self, new_center):
        """Sets the hex in the center of the grid

        :param new_center: coordinate of the center of the grid
        :type new_center: Axial
        """
        self.center_hex = new_center
        window_x = window_y = self.window_size / 2
        offset_center = new_center - self.topleft_corner
        if self.hex_format == 'flat':
            pixelx = self.hex_size * 3 / 2 * offset_center.q
            pixely = self.hex_size * sqrt(3) * (offset_center.r + offset_center.q / 2)
        else:
            pixelx = self.hex_size * sqrt(3) * (offset_center.q + offset_center.r / 2)
            pixely = self.hex_size * 3 / 2 * offset_center.r
        self.xoffset = window_x - pixelx
        self.yoffset = window_y - pixely

    def inside_boundary(self, coord):
        """Checks if a given axial coordinate is inside the grid

        :param coord: coordinate to be tested against the grid
        :type coord: Axial
        :returns: bool - True if inside, False otherwise
        """
        coordx, coordy = coord - self.center_hex
        return (abs(coordx + coordy) <= self.size and
                abs(coordx) <= self.size and
                abs(coordy) <= self.size)

    def hexagon_list(self):
        """A sequence of hexagons

        Hexagons are represented by triplets containing the axial coordinate,
        the center pixel (a 2-tuple), and the corner pixels (a 6-tuple of 2-tuples)
        """
        axial = tuple(p.to_axial()
                      for p in self.center_hex.to_cube().circle_around(self.size))
        centers = tuple(self.get_center(coord) for coord in axial)
        corners = tuple(tuple(self.center_to_corners(center))
                        for center in centers)
        return list(map(Hex, axial, centers, corners))

    def all_centers(self, axial_points):
        """Returns the pixel centers of the axial coordinates given

        Each center is represented as a 2-tuple of floats (pixels)
        """
        for point in axial_points:
            yield self.get_center(point)

    def get_center(self, axial):
        """Converts an axial coordinate to it's pixel center

        :returns: 2-tuple of float
        """
        offset_point = axial - self.topleft_corner
        qcoord, rcoord = offset_point
        if self.hex_format == 'flat':
            centerx = self.hex_size * 3 / 2 * qcoord + self.xoffset
            centery = self.hex_size * sqrt(3) * (rcoord + qcoord / 2) + self.yoffset
        else:
            centerx = self.hex_size * sqrt(3) * (qcoord + rcoord / 2) + self.xoffset
            centery = self.hex_size * 3 / 2 * rcoord + self.yoffset
        return (centerx, centery)

    def center_to_corners(self, center):
        """Converts the pixel center of a hexagon to it's pixel corners
        """
        corner_function = (HexagonGrid._flat_corners if self.hex_format == 'flat'
                           else HexagonGrid._pointy_corners)
        return corner_function(center, self.hex_size)

    def coord_to_corners(self, axial):
        """Converts an axial coordinate to it's pixel corners
        """
        return self.center_to_corners(self.get_center(axial))

    def clicked_hex(self, mousepos):
        """Gets the hexagon clicked

        Calculates which hexagon is in a given window position,
        returns None if no hexagon was clicked

        :param mousepos: point clicked in the window
        :type mousepos: tuple of float
        :returns: Axial or None
        """
        mousex, mousey = mousepos
        mousex = mousex - self.xoffset
        mousey = mousey - self.yoffset
        size = self.hex_size
        if self.hex_format == 'flat':
            hexq = mousex * (2 / 3) / size
            hexr = ((-mousex / 3) + (sqrt(3) / 3) * mousey) / size
        else:
            hexq = (mousex * (sqrt(3) / 3) - (mousey / 3)) / size
            hexr = mousey * ((2 / 3) / size)
        absolute_hex = Axial(hexq, hexr).to_cube().round().to_axial()
        offset_hex = absolute_hex + self.topleft_corner
        if self.inside_boundary(offset_hex):
            return offset_hex
        return None
