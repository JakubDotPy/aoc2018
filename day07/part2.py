import argparse
import os.path
import re
from collections import defaultdict
from functools import lru_cache

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


@lru_cache
class Task:
    done = []

    def __init__(self, name):
        self.name = name
        self.prerequisites = set()
        self.duration = ord(name) - 64 + 60
        self.in_progress = False

    @property
    def can_be_done(self):
        no_prerequisites = not self.prerequisites
        all_prereq_met = self.prerequisites <= set(Task.done)
        not_in_progress = not self.in_progress
        not_done = not self in Task.done
        return not_in_progress and not_done and (all_prereq_met or no_prerequisites)

    def __repr__(self):
        return f'Task({self.name})'

    def __str__(self):
        return self.__repr__()


class Worker:
    def __init__(self, number):
        self.number = number
        self.task = None

    def work(self):
        if not self.task:
            return
        task = self.task
        task.duration -= 1
        if task.duration == 0:
            task.__class__.done.append(task)
            task.in_progress = False
            self.task = None

    def __repr__(self):
        return f'Worker({self.number})'

    def __str__(self):
        return self.__repr__()


def compute(s: str, workers: int) -> int:
    all_tasks = set()

    # collect requirements
    prerequisites = defaultdict(set)
    for row in s.splitlines():
        preq, task = map(Task, re.findall(STEPS_RE, row))
        # create the tasks
        task.prerequisites.add(preq)
        all_tasks |= {preq, task}

    workers = list(Worker(i) for i in range(workers))

    elapsed_time = 0

    header_list = ['Second'] + workers + ['Done']
    # print('\n')
    # print(' '.join(f'{item!s:^8}' for item in header_list))

    while len(Task.done) < len(all_tasks):

        # work on tasks
        for w in workers:
            w.work()

        # find possible tasks and free workers
        possible_tasks = (t for t in all_tasks if t.can_be_done)
        free_workers = (w for w in workers if not w.task)

        # assign to free workers
        assignments = zip(possible_tasks, free_workers)
        for t, w in assignments:
            w.task = t
            t.in_progress = True

        # print stats
        stat = [elapsed_time] + \
               [w.task.name if w.task else '.' for w in workers] + \
               [''.join(t.name for t in Task.done)]
        # print(' '.join(f'{item!s:^8}' for item in stat))

        # progress time
        elapsed_time += 1

    return elapsed_time - 1


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'workers', 'expected'),
    (
            (INPUT_S, 2, 15),
            ),
    )
def test(input_s: str, workers: int, expected: int) -> None:
    assert compute(input_s, workers) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read(), 5))

    return 0


if __name__ == '__main__':
    exit(main())
