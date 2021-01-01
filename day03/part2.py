import argparse
import os.path
import re
from collections import Counter

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""


def compute(s: str) -> int:
    cnt = Counter()

    ROW_RE = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
    rows = re.findall(ROW_RE, s)
    for tile_id, p_x, p_y, w, h in rows:
        tile_id, p_x, p_y, w, h = map(int, (tile_id, p_x, p_y, w, h))
        for x in range(p_x, p_x + w):
            for y in range(p_y, p_y + h):
                cnt[(x, y)] += 1

    single_tile = set(k for k, v in cnt.items() if v == 1)
    for tile_id, p_x, p_y, w, h in rows:
        tile_id, p_x, p_y, w, h = map(int, (tile_id, p_x, p_y, w, h))

        if all(
                (x, y) in single_tile
                for x in range(p_x, p_x + w)
                for y in range(p_y, p_y + h)
                ):
            return tile_id


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 3),
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
