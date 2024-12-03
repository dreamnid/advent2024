#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul, ge, gt, itemgetter, le, lt
import os
import pprint
import re
from time import time
from typing import NamedTuple

from humanize import intcomma
import numpy as np
import pyparsing as pp
import pandas as pd

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='3-input.txt'
# INPUT_FILE='3a-example.txt'
# INPUT_FILE='3b-example.txt'

input = ''.join(get_file_contents(INPUT_FILE)[0])
mul_raw_regex = r'mul\((\d+),(\d+)\)'
mul_regex = re.compile(mul_raw_regex)
print('a:', sum([int(x) * int(y) for x, y in mul_regex.findall(input)]))

def part_2():
    status = True
    buf = input
    start = 0

    res: list[int] = []
    while True:
        end = remain_len = len(buf) - 1
        if status:
            try:
                end = buf.index("don't()", start, end) + len("don't()")
                next_status = False
            except ValueError:
                end = remain_len

            res.extend([int(x) * int(y) for x, y in mul_regex.findall(buf[:end], start, end)])
        else:
            try:
                end = buf.index("do()", start, end) + len("do()")
                next_status = True
            except ValueError:
                end = remain_len

        if end == remain_len:
            break

        start = end
        status = next_status
    return res

def part_2_alt():
    enabled = True

    matcher = re.compile(r"do\(\)|don't\(\)|" + mul_raw_regex)
    res = 0
    for cur_match in matcher.finditer(input):
        match cur_match.group():
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _:
                res += int(cur_match.group(1)) * int(cur_match.group(2)) if enabled else 0
    return res

print('b:', part_2_alt())
