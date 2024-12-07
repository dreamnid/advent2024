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

INPUT_FILE='7-input.txt'
# INPUT_FILE='7a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

def solver(nums: list[int], desired: int, cur_answer: int):
    cur_answer = nums.pop(0)

    queue = [(nums, cur_answer)]

    while queue:
        nums, cur_answer = queue.pop(0)

        if not nums:
            if cur_answer == desired:
                return True
            elif queue:
                continue
            else:
                return False

        cur_num = nums.pop(0)
        add_answer = cur_num + cur_answer
        if add_answer <= desired:
            queue.append((nums.copy(), add_answer))

        mul_answer = cur_answer * cur_num
        if mul_answer <= desired:
            queue.append((nums.copy(), mul_answer))

    return False

res = 0
for eq_i, eq in enumerate(input):
    desired, nums = eq.split(': ')
    desired_int = int(desired)
    temp_res = solver([int(num) for num in nums.split(' ')], desired_int, 0)
    if temp_res:
        res += desired_int


print('a:', res)

