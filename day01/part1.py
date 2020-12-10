import argparse
import os.path

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    return sum(int(num) for num in s.splitlines())


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('+1\n-2\n+3\n+1', 3),
            ('+1\n+1\n+1', 3),
            ('+1\n+1\n-2', 0),
            ('-1\n-2\n-3', -6),
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
