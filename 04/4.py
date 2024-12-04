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

INPUT_FILE='4-input.txt'
# INPUT_FILE='4a-example.txt'
# INPUT_FILE='4a2-example.txt'

def checker(matrix: list[str], cur_row: int, cur_col: int):
    return [
        checker_helper(matrix, cur_row, cur_col, row_incr=0, col_incr=1),
        checker_helper(matrix, cur_row, cur_col, row_incr=0, col_incr=-1),
        checker_helper(matrix, cur_row, cur_col, row_incr=1, col_incr=0),
        checker_helper(matrix, cur_row, cur_col, row_incr=-1, col_incr=0),
        checker_helper(matrix, cur_row, cur_col, row_incr=1, col_incr=1),
        checker_helper(matrix, cur_row, cur_col, row_incr=-1, col_incr=-1),
        checker_helper(matrix, cur_row, cur_col, row_incr=1, col_incr=-1),
        checker_helper(matrix, cur_row, cur_col, row_incr=-1, col_incr=1),
        ]

def checker_helper(matrix: list[str], cur_row: int, cur_col: int, row_incr: int, col_incr: int):
    CHECK_WORD = 'XMAS'
    for i in range(len(CHECK_WORD)):
        if matrix[cur_row+i*row_incr][cur_col+i*col_incr] != CHECK_WORD[i]:
            return False
    return True

# Add padding and upper case input
input = ['.'*5+line.upper()+'.'*5 for line in get_file_contents(INPUT_FILE)[0]]
input = ['.'*len(input[0])] * 5 + input + ['.'*len(input[0])] * 5

res = []
for row_i, row in enumerate(input):
    for col_i, col in enumerate(row):
        if 'X' == col:
            res.extend(checker(input, row_i, col_i))

print('a:', sum(res))
