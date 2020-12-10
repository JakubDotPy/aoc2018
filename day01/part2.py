import argparse
import os.path
from itertools import cycle

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    seen = {0}
    partial_sum = 0
    for num in map(int, cycle(s.splitlines())):
        partial_sum += num
        if partial_sum not in seen:
            seen.add(partial_sum)
        else:
            return partial_sum


@pytest.mark.complete
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('+1\n-1', 0),
            ('+3\n3\n4\n-2\n-4', 10),
            ('-6\n3\n8\n5\n-6', 5),
            ('+7\n7\n-2\n-7\n-4', 14),
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
