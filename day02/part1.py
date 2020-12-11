import argparse
import os.path
from collections import Counter

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab"""


def compute(s: str) -> int:
    twos = 0
    threes = 0

    for word in s.splitlines():
        counts = Counter(word)

        threes += 3 in counts.values()
        twos += 2 in counts.values()

    return threes * twos


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 12),
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
