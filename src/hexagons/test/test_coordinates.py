"""
Test module for coordinate methods and conversions
"""


import hexagons.coordinate as coord


def test_cube_getters():
    c = coord.Cube(1, 0, -3)
    assert c.x == 1
    assert c.y == 0
    assert c.z == -3


def test_cube_to_axis():
    assert coord.Cube(1, 2, 3).to_axial() == coord.Axial(1, 3)
    assert coord.Cube(-2, 2, 5).to_axial() == coord.Axial(-2, 5)
