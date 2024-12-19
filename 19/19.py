#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from functools import partial, reduce
from itertools import chain, cycle, takewhile, permutations
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

INPUT_FILE='19-input.txt'
# INPUT_FILE='19a-example.txt'


@dataclass
class Data:
    design: str
    avail: dict


file_contents = get_file_contents(INPUT_FILE)
towels = dict(Counter(file_contents[0][0].split(', ')))
first_letter_towels = defaultdict(list)

for towel in towels:
    first_letter_towels[towel[0]].append(towel)

# print(towels)
count = 0
for desired_i, desired in enumerate(file_contents[1]):
    # print(desired_i, 'desired:', desired, end='')
    # https://www.hellointerview.com/learn/code/dynamic-programming/word-break#alternative-solution
    dp = [False] * (len(desired) + 1)
    dp[0] = True

    for i in range(1, len(desired) + 1):
        for towel in towels:
            if i >= len(towel) and dp[i-len(towel)]:
                sub = desired[i-len(towel):i]
                if sub == towel:
                    dp[i] = True
                    break
    if dp[len(desired)]:
        count += 1
        # print(' found', end='')
    # print()
    # queue = [Data('', towels)]
    # while queue:
    #     cur_data = queue.pop()
    #     used_towels = [cur_towel for cur_towel in first_letter_towels[desired[len(cur_data.design)]]
    #                    if desired[len(cur_data.design):].startswith(cur_towel)
    #                    ]
    #     # used_towels = [cur_towel for cur_towel, towel_cnt in cur_data.avail.items()
    #     #                if desired[len(cur_data.design):].startswith(cur_towel)
    #     #                ]
    #     for cur_towel in used_towels:
    #         if cur_data.design + cur_towel == desired:
    #             count += 1
    #             queue = []
    #             print(' found!', end='')
    #             break
    #         new_towels = cur_data.avail.copy()
    #         new_towels[cur_towel] -= 1
    #         queue.append(Data(cur_data.design + cur_towel, new_towels))
    # print()

print('a', count)
