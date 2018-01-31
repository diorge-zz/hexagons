"""
Test module for coordinate methods and conversions
"""


import hexagons.coordinate as coord
import pytest
import itertools


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


def test_cube_diagonals():
    c = coord.Cube(1, 0, -1)
    n = list(c.diagonals())
    assert len(n) == 6
    assert coord.Cube(3, -1, -2) in n
    assert coord.Cube(-1, 1, 0) in n
    assert coord.Cube(0, 2, -2) in n
    assert coord.Cube(2, -2, 0) in n
    assert coord.Cube(0, -1, 1) in n
    assert coord.Cube(2, 1, -3) in n


def test_cube_distance():
    c = coord.Cube(0, 0, 0)
    assert 0 == c.distance(c)
    assert all(1 == c.distance(n) for n in c.neighbors())
    assert 4 == c.distance(coord.Cube(-1, 4, -3))


def test_cube_round_simple():
    c = coord.Cube(0.1, 1.8, -1.9)
    assert c.round() == coord.Cube(0, 2, -2)


def test_cube_round_edge():
    c = coord.Cube(0.4, 0.3, -0.7)
    assert c.round() == coord.Cube(1, 0, -1)


def test_line():
    origin = coord.Cube(0, 0, 0)
    target = coord.Cube(2, -4, 2)
    hexes_in_line = [origin, coord.Cube(1, -1, 0), coord.Cube(1, -2, 1),
                     coord.Cube(2, -3, 1), target]
    line = origin.line_to(target)
    assert set(hexes_in_line) == set(line)


def test_line_order():
    """ The line must be draw in the order from origin to target """
    origin = coord.Cube(0, 0, 0)
    target = coord.Cube(-3, 1, 2)
    hexes_in_line = [origin, coord.Cube(-1, 0, 1), coord.Cube(-2, 1, 1),
                     target]
    line = list(origin.line_to(target))
    assert hexes_in_line == line


def test_circle_around():
    center = coord.Cube(0, 0, 0)
    immediate = list(center.neighbors())
    dist2 = [list(imm.neighbors()) for imm in immediate]
    flat_dist2 = itertools.chain(*dist2)
    everything = set([center]) | set(immediate) | set(flat_dist2)
    assert everything == set(center.circle_around(2))


def test_circle_around_with_obstacles():
    center = coord.Cube(0, 0, 0)
    obstacles = [(1, 0, -1), (2, -1, -1), (2, -2, 0), (2, -3, 1), (1, -3, 2),
                 (0, -2, 2), (-1, -1, 2), (-1, 0, 1), (-2, 1, 1), (-3, 1, 2),
                 (-4, 1, 3), (-5, 1, 4), (1, 2, -3), (0, 2, -2), (-1, 2, -1)]
    expected_within_3 = [center, (1, -1, 0), (1, -2, 1), (0, -1, 1),
                         (0, 1, -1), (1, 1, -2), (2, 1, -3), (2, 0, -2),
                         (-1, 1, 0), (-2, 2, 0), (-3, 3, 0), (-2, 3, -1),
                         (-3, 2, 1)]
    obstacles = set(map((lambda d: coord.Cube(*d)), obstacles))
    expected_within_3 = set(map((lambda d: coord.Cube(*d)), expected_within_3))
    result = set(center.circle_around(3, lambda x: x in obstacles))
    assert expected_within_3 == result


def test_rotate_right():
    center = coord.Cube(2, 0, -2)
    torotate = coord.Cube(4, -1, -3)
    expected = [coord.Cube(3, -2, -1), coord.Cube(1, -1, 0),
                coord.Cube(0, 1, -1), coord.Cube(1, 2, -3),
                coord.Cube(3, 1, -4), coord.Cube(4, -1, -3)]
    result = [torotate.rotate_right(center, i) for i in range(1, 7)]
    assert expected == result


def test_rotate_left():
    center = coord.Cube(2, 0, -2)
    torotate = coord.Cube(4, -1, -3)
    expected = [coord.Cube(3, 1, -4), coord.Cube(1, 2, -3),
                coord.Cube(0, 1, -1), coord.Cube(1, -1, 0),
                coord.Cube(3, -2, -1), coord.Cube(4, -1, -3)]
    result = [torotate.rotate_left(center, i) for i in range(1, 7)]
    assert expected == result


def test_circumference():
    center = coord.Cube.origin
    expected = set([coord.Cube(2, -2, 0), coord.Cube(2, -1, -1),
                   coord.Cube(2, 0, -2), coord.Cube(1, 1, -2),
                   coord.Cube(0, 2, -2), coord.Cube(-1, 2, -1),
                   coord.Cube(-2, 2, 0), coord.Cube(-2, 1, 1),
                   coord.Cube(-2, 0, 2), coord.Cube(-1, -1, 2),
                   coord.Cube(0, -2, 2), coord.Cube(1, -2, 1)])
    result = set(center.circumference(2))
    assert expected == result


def test_circumference_zero():
    center = coord.Cube(1, 1, -2)
    result = list(center.circumference(0))
    assert [center] == result


def test_circumference_one():
    center = coord.Cube(5, -6, 1)
    assert set(center.neighbors()) == set(center.circumference(1))


def test_circumference_nonorigin():
    center = coord.Cube(1, 0, -1)
    expected = set([coord.Cube(3, -2, -1), coord.Cube(3, -1, -2),
                    coord.Cube(3, 0, -3), coord.Cube(2, 1, -3),
                    coord.Cube(1, 2, -3), coord.Cube(0, 2, -2),
                    coord.Cube(-1, 2, -1), coord.Cube(-1, 1, 0),
                    coord.Cube(-1, 0, 1), coord.Cube(0, -1, 1),
                    coord.Cube(1, -2, 1), coord.Cube(2, -2, 0)])
    result = set(center.circumference(2))
    assert expected == result


def test_basic_ray_vision():
    center = coord.Cube.origin
    obstacles = set([coord.Cube(0, -1, 1), coord.Cube(2, 0, -2)])
    expected = set(center.circle_around(3))
    expected.remove(coord.Cube(0, -2, 2))
    expected.remove(coord.Cube(-1, -2, 3))
    expected.remove(coord.Cube(0, -3, 3))
    expected.remove(coord.Cube(1, -3, 2))
    expected.remove(coord.Cube(3, 0, -3))
    result = set(center.basic_ray_vision(lambda x: x in obstacles, size=3))
    assert expected == result


def test_arc():
    center = coord.Cube.origin
    facing_direction = coord.Cube(1, 0, -1)
    expected = set([coord.Cube(3, -3, 0), coord.Cube(3, -2, -1),
                    coord.Cube(3, -1, -2), coord.Cube(3, 0, -3),
                    coord.Cube(2, 1, -3), coord.Cube(1, 2, -3),
                    coord.Cube(0, 3, -3)])
    result = set(center.arc(facing_direction, 3))
    assert expected == result


def test_facing_ray_vision():
    center = coord.Cube.origin
    facing_direction = coord.Cube(1, 0, -1)
    size = 3
    obstacle = coord.Cube(1, 0, -1)
    expected = set([coord.Cube(0, 3, -3), coord.Cube(0, 2, -2),
                    coord.Cube(0, 1, -1), coord.Cube(1, -1, 0),
                    coord.Cube(2, -2, 0), coord.Cube(3, -3, 0),
                    coord.Cube(1, 2, -3), coord.Cube(1, 1, -2),
                    coord.Cube(3, -2, -1), coord.Cube(2, -1, -1),
                    # the wall and the player are also visible
                    coord.Cube(1, 0, -1), center])
    result = center.facing_ray_vision(facing_direction, size,
                                      lambda x: x == obstacle)
    assert expected == result
