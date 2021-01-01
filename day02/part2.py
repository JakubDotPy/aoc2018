import argparse
import os.path

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"""


def compute(s: str) -> int:
    # sliding window
    back = 0

    words = s.splitlines()

    for word in words[back:]:
        front = back + 1
        while front != len(words):
            next_word = words[front]
            differences = sum(c_1 != c_2 for c_1, c_2 in zip(word, next_word))
            if differences == 1:
                return ''.join(c_1 for c_1, c_2 in zip(word, next_word) if c_1 == c_2)
            front += 1
        back += 1


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 'fgij'),
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
