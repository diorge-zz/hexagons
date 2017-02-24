"""
Test module for grids
"""


import hexagons.grid as grid
from hexagons.coordinate import Axial


def test_hexagonal_grid_boundaries():
    g = grid.HexagonGrid(size=3)
    assert g.inside_boundary(Axial(3, 0))
    assert g.inside_boundary(Axial(0, 3))
    assert g.inside_boundary(Axial(3, -3))
    assert g.inside_boundary(Axial(0, 0))
    assert not g.inside_boundary(Axial(3, 1))
