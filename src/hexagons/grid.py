"""
Module grid
Grids for hexagons
"""


class HexagonGrid:
    """
    Hexagonal grid of hexagonal tiles
    """

    def __init__(self, size):
        self.size = size

    def inside_boundary(self, coord):
        """ Checks if a given axial coordinate is inside the grid """
        x, y = coord.q, coord.r
        return abs(x + y) <= self.size
