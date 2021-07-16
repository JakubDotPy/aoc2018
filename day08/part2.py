import argparse
import os.path

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
"""


class Node:

    def __init__(self, series: list):
        self.num_ch = series.pop(0)
        self.num_md = series.pop(0)

        self.children = [Node(series) for _ in range(self.num_ch)]
        self.metadata = [series.pop(0) for _ in range(self.num_md)]

    def sum_md(self):
        if not self.children:
            return sum(self.metadata)
        else:
            total = 0
            for i in self.metadata:
                try:
                    total += self.children[i - 1].sum_md()
                except IndexError:
                    pass
            return total


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2', 66),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def compute(s: str) -> int:
    input_list = list(map(int, s.split()))
    root = Node(input_list)
    return root.sum_md()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
