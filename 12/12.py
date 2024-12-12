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

INPUT_FILE='12-input.txt'
# INPUT_FILE='12a-example.txt'
# INPUT_FILE='12a2-example.txt'

input = add_padding([line for line in get_file_contents(INPUT_FILE)[0]])

def calc_perimeter(row_i: int, col_i: int, cur_char: str):
    perim = 0
    area = 1
    visited.add((row_i, col_i))
    if input[row_i][col_i-1] == cur_char:
        if (row_i, col_i-1) not in visited:
            cur_area, cur_perim = calc_perimeter(row_i, col_i-1, cur_char)
            perim += cur_perim
            area += cur_area
    else:
        perim += 1
    if input[row_i+1][col_i] == cur_char:
        if (row_i+1, col_i) not in visited:
            cur_area, cur_perim = calc_perimeter(row_i+1, col_i, cur_char)
            perim += cur_perim
            area += cur_area
    else:
        perim += 1
    if input[row_i][col_i+1] == cur_char:
        if (row_i, col_i+1) not in visited:
            cur_area, cur_perim = calc_perimeter(row_i, col_i+1, cur_char)
            perim += cur_perim
            area += cur_area
    else:
        perim += 1
    if input[row_i-1][col_i] == cur_char:
        if (row_i-1, col_i) not in visited:
            cur_area, cur_perim = calc_perimeter(row_i-1, col_i, cur_char)
            perim += cur_perim
            area += cur_area
    else:
        perim += 1

    return area, perim

visited = set()
areas = defaultdict(int)
perimeters = defaultdict(int)
regions = list()
for row_i, row in enumerate(input):
    for col_i, val in enumerate(row):
        if val != '.':
            if (row_i, col_i) not in visited:
                regions.append((val, *calc_perimeter(row_i, col_i, val)))
            areas[val] += 1

        visited.add((row_i, col_i))

print('areas')
pprint.pprint(areas)
print('perim')
pprint.pprint(perimeters)
print('regions')
pprint.pprint(regions)
print('a:', sum([area * perim for _, area, perim in regions]))
