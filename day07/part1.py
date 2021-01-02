import argparse
import os.path
import re
from collections import defaultdict

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

STEPS_RE = re.compile(r' ([A-Z]) ')


def compute(s: str) -> str:
    steps = set()
    prerequisites = defaultdict(set)
    for row in s.splitlines():
        start, end = re.findall(STEPS_RE, row)
        steps |= {start, end}
        prerequisites[end].add(start)

    done = []
    for _ in steps:
        can_be_done = lambda step: step not in done and prerequisites[step] <= set(done)
        candidates = (s for s in steps if can_be_done(s))
        done.append(min(candidates))  # add the step by alphabet

    return ''.join(done)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 'CABDFE'),
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
