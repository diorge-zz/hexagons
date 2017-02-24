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


def test_axial_getters():
    c = coord.Axial(1, -1)
    assert c.q == 1
    assert c.r == -1


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


def test_iterable_cube():
    c = coord.Cube(-2, 0, 2)
    x, y, z = c
    assert (c.x, c.y, c.z) == (x, y, z)


def test_iterable_axial():
    c = coord.Axial(3, 5)
    q, r = c
    assert (c.q, c.r) == (q, r)


def test_cube_neighbors():
    c = coord.Cube(0, 0, 0)
    n = list(c.neighbors())
    assert len(n) == 6
    assert coord.Cube(1, -1, 0) in n
    assert coord.Cube(1, 0, -1) in n
    assert coord.Cube(0, 1, -1) in n
    assert coord.Cube(-1, 1, 0) in n
    assert coord.Cube(-1, 0, 1) in n
    assert coord.Cube(0, -1, 1) in n


def test_axial_neighbors():
    c = coord.Axial(5, 5)
    n = list(c.neighbors())
    assert len(n) == 6
    assert coord.Axial(6, 5) in n
    assert coord.Axial(6, 4) in n
    assert coord.Axial(5, 4) in n
    assert coord.Axial(4, 5) in n
    assert coord.Axial(4, 6) in n
    assert coord.Axial(5, 4) in n
