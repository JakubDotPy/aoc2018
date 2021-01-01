import argparse
import os.path
import re
from collections import Counter, defaultdict
from datetime import datetime
from datetime import timedelta

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""


def parse(s):
    ROW_RE = re.compile(r'\[(.*)\] (.*)')
    reusult = list(
        (datetime.strptime(when_s, '%Y-%m-%d %H:%M'), what_s)
        for when_s, what_s in re.findall(ROW_RE, s)
        )
    return sorted(reusult, key=lambda x: x[0])


def compute(s: str) -> int:
    events = parse(s)
    guards_sleeping = defaultdict(list)

    for event in events:
        when, what = event
        if what.startswith('Guard'):
            current_guard_id = int(re.findall(r'\d+', what)[0])
            continue
        if what == 'falls asleep':
            falls_asleep = when
            continue
        if what == 'wakes up':
            wakes_up = when
            guards_sleeping[current_guard_id].append((falls_asleep, wakes_up))
            continue

    sleep_counter = Counter()
    for guard, sleeps in guards_sleeping.items():
        for sleep_start, sleep_end in sleeps:
            sleep_counter[guard] += (sleep_end - sleep_start).seconds // 60

    most_asleep_id = max(sleep_counter, key=sleep_counter.get)

    minute_counter = Counter()
    for sleep_start, sleep_end in guards_sleeping[most_asleep_id]:
        while sleep_start < sleep_end:
            minute_counter[sleep_start.minute] += 1
            sleep_start += timedelta(minutes=1)

    overlapping_minute = max(minute_counter, key=minute_counter.get)

    return most_asleep_id * overlapping_minute


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 240),
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
