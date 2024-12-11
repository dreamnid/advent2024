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

INPUT_FILE='11-input.txt'
# INPUT_FILE='11a-example.txt'
# INPUT_FILE='11a2-example.txt'
# INPUT_FILE='11bg1-example.txt'

input = [int(num) for line in get_file_contents(INPUT_FILE)[0] for num in line.split(' ')]
print(input)

MAP = {
    0: (1, [1]),
    1: (3, [2, 0, 2, 4]),
    2: (3, [4, 0, 4, 8]),
    3: (3, [6, 0, 7, 2]),
    4: (3, [8, 0, 9, 6]),
    5: (5, [2, 0, 4, 8, 2, 8, 8, 8]),
    6: (5, [2, 4, 5, 7, 9, 4, 5, 6]),
    7: (5, [2, 8, 6, 7, 6, 0, 3, 2]),
    8: (5, [3, 2, 7, 7, 2, 6, 16192]),
    9: (5, [3, 6, 8, 6, 9, 1, 8, 4]),
}

def step(input: list):
    res = []
    for i, stone in enumerate(input):
        if stone == 0:
            res.append(1)
        elif len((str_num := str(stone))) % 2 == 0:
            half = len(str_num) // 2
            res.append(int(str_num[0:half]))
            res.append(int(str_num[half:]))
        else:
            res.append(stone * 2024)

    return res

with PrintTiming('a'):
    cur_input = input.copy()
    for i in range(25):
        cur_input = step(cur_input)

print('a:', len(cur_input))

def step2(input: list):
    res = 0
    for i, stone in enumerate(input):
        cur_stone_res = [stone]
        # print(cur_stone_res)
        for j in range(75):
            cur_stone_res = step(cur_stone_res)
            print('stone j', j)
        res += len(cur_stone_res)
        print('i', i)
    return res

# with PrintTiming('b'):
#     cur_input = input.copy()
#     res = step2(cur_input)
# print('b:', res)
