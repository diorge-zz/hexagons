"""
Test module for hexagons
"""


import hexagons.grid as grid


def test_hexagonal_grid_boundaries():
    g = grid.HexagonGrid(size=3)
    assert g.inside_boundary((3, 0))
    assert g.inside_boundary((0, 3))
    assert g.inside_boundary((3, -3))
    assert g.inside_boundary((0, 0))
    assert not g.inside_boundary((3, 1))
