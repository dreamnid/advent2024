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

INPUT_FILE='15-input.txt'
# INPUT_FILE='15a-example.txt'
# INPUT_FILE='15a2-example.txt'

input = [[char for char in line] for line in get_file_contents(INPUT_FILE)[0]]
# pprint.pprint(input)

for row_i, row in enumerate(input):
    try:
        col_i = row.index('@')
        robot = (row_i, col_i)
        break
    except ValueError:
        pass

def get_movement_for_dir(dir: str):
    """Returns the number of rows and number of cols respectively"""
    match dir:
        case '^':
            return -1, 0
        case '>':
            return 0, 1
        case 'v':
            return 1, 0
        case '<':
            return 0, -1


def move_pos(input, old_pos, new_pos):
    input[new_pos[0]][new_pos[1]] = input[old_pos[0]][old_pos[1]]
    input[old_pos[0]][old_pos[1]] = '.'


directions = [char for line in get_file_contents(INPUT_FILE)[1] for char in line]

with PrintTiming('a'):
    for dir_i, dir in enumerate(directions):
        movement = get_movement_for_dir(dir)

        new_pos = robot[0] + movement[0], robot[1] + movement[1]
        match input[new_pos[0]][new_pos[1]]:
            case '.':
                move_pos(input, robot, new_pos)
                robot = new_pos
            case 'O':
                steps: list[tuple[tuple[int, int], tuple[int, int]]] = [(robot, new_pos)]
                cur_temp_pos = new_pos
                while True:
                    new_temp_pos = cur_temp_pos[0] + movement[0], cur_temp_pos[1] + movement[1]
                    steps.append((cur_temp_pos, new_temp_pos))
                    match input[new_temp_pos[0]][new_temp_pos[1]]:
                        case '.':
                            # Shift boxes
                            for cur_step in steps[::-1]:
                                move_pos(input, cur_step[0], cur_step[1])
                            robot = cur_step[1]
                            break
                        case 'O':
                            # Keep stepping
                            pass
                        case '#':
                            break
                    cur_temp_pos = new_temp_pos

        if dir_i % 10 == 0 and False:
            print(dir_i, dir)
            pprint.pprint(input)

    # pprint.pprint(input)
    # input = ['#######', '#...O..', '#......']

    res = [(row_i * 100 + col_i) for row_i, row in enumerate(input) for col_i, col in enumerate(row) if col == 'O']
print('a:', sum(res))
