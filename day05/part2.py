import argparse
import os.path
import re
from string import ascii_lowercase

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
dabAcCaCBAcCcaDA"""

DOUBLE_RE = re.compile(
    r'(Aa|Bb|Cc|Dd|Ee|Ff|Gg|Hh|Ii|Jj|Kk|Ll|Mm|Nn|Oo|Pp|Qq|Rr|Ss|Tt|Uu|Vv|Ww|Xx|Yy|Zz|'
    r'aA|bB|cC|dD|eE|fF|gG|hH|iI|jJ|kK|lL|mM|nN|oO|pP|qQ|rR|sS|tT|uU|vV|wW|xX|yY|zZ)'
    )


def reduce_polymer(s):
    while re.findall(DOUBLE_RE, s):
        s = re.sub(DOUBLE_RE, '', s)
    return s


def compute(s: str) -> int:
    shortest = 999_999
    old_s = s
    for letter in ascii_lowercase:
        same_re = re.compile(f'({letter})', flags=re.IGNORECASE)
        prepared_s = re.sub(same_re, '', old_s)
        reduced_s = reduce_polymer(prepared_s)
        if (new_short := len(reduced_s)) < shortest:
            shortest = new_short

    return shortest


@pytest.mark.complete
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 4),
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
