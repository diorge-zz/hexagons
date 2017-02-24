"""
Test module for coordinate methods and conversions
"""


import hexagons.coordinate as coord
import pytest


def test_cube_getters():
    c = coord.Cube(1, 0, -1)
    assert c.x == 1
    assert c.y == 0
    assert c.z == -1


def test_cube_to_axis():
    assert coord.Cube(1, 2, -3).to_axial() == coord.Axial(1, -3)
    assert coord.Cube(-2, -3, 5).to_axial() == coord.Axial(-2, 5)


def test_axis_to_cube():
    assert coord.Axial(1, -3).to_cube() == coord.Cube(1, 2, -3)
    assert coord.Axial(-2, 5).to_cube() == coord.Cube(-2, -3, 5)


def test_invalid_cube():
    """ Cubes are invalid if they don't slice the x+y+z=0 plane """
    with pytest.raises(ValueError):
        c = coord.Cube(1, 2, 3)
