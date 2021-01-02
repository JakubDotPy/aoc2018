import argparse
import os.path
from collections import defaultdict
from string import ascii_letters

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

map_test = """
..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.

    0123456789
  0 aaaaa.cccc
  1 aAaaa.cccc
  2 aaaddecccc
  3 aadddeccCc
  4 ..dDdeeccc
  5 bb.deEeecc
  6 bBb.eeee..
  7 bbb.eeefff
  8 bbb.eeffff
  9 bbb.ffffFf
  
    12345678
  1 Aaaa.ccc
  2 aaddeccc
  3 adddeccC
  4 .dDdeecc
  5 b.deEeec
  6 Bb.eeee.
  7 bb.eeeff
  8 bb.eefff
  9 bb.ffffF
  
"""


def assign_letter(point, points):
    distances = dict()
    p_x, p_y = point
    for name, (c_x, c_y) in points.items():
        dist = abs(p_x - c_x) + abs(p_y - c_y)
        distances[name] = dist

    min_dist = min(distances.values())
    if list(distances.values()).count(min_dist) == 1:
        return next(k for k, v in distances.items() if v == min_dist)
    else:
        return '.'


def compute(s: str) -> int:
    waypoint_tuples = set(
        tuple(map(int, row.split(', ')))
        for row in s.splitlines()
        )
    waypoints = dict(
        (letter, coords) for letter, coords in zip(ascii_letters, waypoint_tuples)
        )

    x_coords = set(x for x, y in waypoint_tuples)
    y_coords = set(y for x, y in waypoint_tuples)
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    points = dict()
    for point_x in range(min_x, max_x + 1):
        for point_y in range(min_y, max_y + 1):
            point = (point_x, point_y)
            points[point] = assign_letter(point, waypoints)

    areas = defaultdict(list)
    for coord, name in points.items():
        if name == '.':
            continue
        areas[name].append(coord)

    to_delete = set()
    for name, coords in areas.items():
        for (x, y) in coords:
            if x in (min_x, max_x) or y in (min_y, max_y):
                to_delete.add(name)

    maximal_area = max(len(v) for k, v in areas.items() if k not in to_delete)

    return maximal_area


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 17),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
