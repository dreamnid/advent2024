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

INPUT_FILE='25-input.txt'
# INPUT_FILE='25a-example.txt'

file_contents = get_file_contents(INPUT_FILE)

locks = []
keys = []
num_cols = len(file_contents[0][0])
total_height = len(file_contents[0])
for schematic in file_contents:
    if '#' * len(schematic[0]) == schematic[0]:
        pin_heights = [None] * len(schematic[0])
        for row_i, row in enumerate(schematic):
            for col_i, col in enumerate(row):
                if col == '.' and pin_heights[col_i] is None:
                    pin_heights[col_i] = row_i - 1
        locks.append(tuple(pin_heights))
    else:
        key_heights = [None] * len(schematic[0])
        for row_i, row in enumerate(schematic):
            for col_i, col in enumerate(row):
                if col == '#' and key_heights[col_i] is None:
                    key_heights[col_i] = len(schematic) - row_i - 1
        keys.append(tuple(key_heights))

# print('locks')
# pprint.pprint(locks)
# print('keys')
# pprint.pprint(keys)

valid_combos = 0
seen = set()
for lock in set(locks):
    for key in set(keys):
        fits = True
        for i in range(num_cols):
            if lock[i] + key[i] > 5:
                fits = False
                break

        if fits:
            seen.add((tuple(lock), tuple(key),))

print('a', len(seen))

