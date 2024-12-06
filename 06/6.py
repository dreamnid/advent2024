#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
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

INPUT_FILE='6-input.txt'
# INPUT_FILE='6a-example.txt'


class Dir(Enum):
    UP = '^'
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'


def get_dir_addr(my_dir: Dir):
    match my_dir:
        case Dir.UP:
            return (-1, 0)
        case Dir.RIGHT:
            return (0, 1)
        case Dir.DOWN:
            return (1, 0)
        case Dir.LEFT:
            return (0, -1)
    return None

input = add_padding([[char for char in line] for line in get_file_contents(INPUT_FILE)[0]], '@')
orig_pos = None
cur_pos = None

cur_dir = None
for row_i, row in enumerate(input):
    for col_i, col in enumerate(row):
        if col not in ['.', '#', '@']:
            cur_pos = orig_pos = (row_i, col_i)
            cur_dir = orig_dir = Dir(col)
            cur_val = orig_val = col
            break

print(cur_dir, cur_pos)

def solver(cur_input: list[list[str]], cur_pos, cur_val: str, cur_dir: Dir):
    visited = defaultdict(set)
    """pos -> list of dir"""

    num_pos = 1
    dir_vals = list(Dir)
    while cur_val != '@':
        next_pos_addr = get_dir_addr(cur_dir)
        next_pos = cur_pos[0] + next_pos_addr[0], cur_pos[1] + next_pos_addr[1]
        next_char = cur_input[next_pos[0]][next_pos[1]]
        match next_char:
            case '.':
                num_pos += 1
                cur_char = next_char
                cur_pos = next_pos
                cur_input[next_pos[0]][next_pos[1]] = 'X'
            case 'X':
                visited[cur_pos].add(cur_dir)
                cur_char = next_char
                cur_pos = next_pos
            case '#':
                cur_dir = dir_vals[(dir_vals.index(cur_dir) + 1) % 4]
                # print('new dir', cur_dir)
            case '@':
                cur_char = next_char
                break
            case _:
                # starting pos
                cur_char = next_char
                cur_pos = next_pos
        if cur_pos in visited and cur_dir in visited[cur_pos]:
            return None
    return num_pos

with PrintTiming('a'):
    print('a:', solver(input, cur_pos, cur_val, cur_dir))

with PrintTiming('b'):
    num_loops = 0
    for row_i, row in enumerate(input):
        for col_i, col in enumerate(row):
            if col == 'X':
                # Make a copy and make current position an obstable
                new_input = deepcopy(input)
                new_input[row_i][col_i] = '#'
                if solver(new_input, orig_pos, orig_val, orig_dir) is None:
                    num_loops += 1

print('b:', num_loops)
