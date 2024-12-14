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

INPUT_FILE = '14-input.txt'
total_rows = 103
total_cols = 101

# INPUT_FILE='14a-example.txt'
# total_rows = 7
# total_cols = 11


class Position(NamedTuple):
    row: int
    col: int


class Distance(NamedTuple):
    rows: int
    cols: int


@dataclass
class Robot:
    pos: Position
    velocity: Distance

    def move(self):
        self.pos = Position((self.pos.row + self.velocity.rows + total_rows) % total_rows,
                            (self.pos.col + self.velocity.cols + total_cols) % total_cols)
        return self.pos


def count_robots_in_quadrants(robots, total_rows, total_cols):
    num_rows_in_quad = total_rows // 2
    num_cols_in_quad = total_cols // 2

    quad_start_positions = (Position(0, 0),
                            Position(total_rows - num_rows_in_quad, 0),
                            Position(0, total_cols - num_cols_in_quad),
                            Position(total_rows - num_rows_in_quad, total_cols - num_cols_in_quad))

    res: list[list[Robot]] = []
    for cur_quad in quad_start_positions:
        cur_quad_res: list[Robot] = [robot for robot in robots if cur_quad.row <= robot.pos.row < cur_quad.row + num_rows_in_quad and cur_quad.col <= robot.pos.col < cur_quad.col + num_cols_in_quad]
        res.append(len(cur_quad_res))

    return res


digit = re.compile(r'-?\d+')

robots: list[Robot] = []
for line in get_file_contents(INPUT_FILE)[0]:
    digits = digit.findall(line)
    robots.append(Robot(Position(int(digits[1]), int(digits[0])), Distance(int(digits[3]), int(digits[2]))))

# pprint.pprint(robots)
with PrintTiming('a'):
    for i in range(100):
        [robot.move() for robot in robots]

print('a:', math.prod(count_robots_in_quadrants(robots, total_rows, total_cols)))

robots.clear()
for line in get_file_contents(INPUT_FILE)[0]:
    digits = digit.findall(line)
    robots.append(Robot(Position(int(digits[1]), int(digits[0])), Distance(int(digits[3]), int(digits[2]))))

Y_AXIS_COL = 50

found = False
counter = 0
max_len_num_of_col_by_row = 100000
with PrintTiming('b'):
    while not found:
        counter += 1
        # if counter % 100 == 0:
        #     print(counter)
        # found = True
        col_by_row = defaultdict(set)
        # new_pos = [robot.pos for robot in robots]
        new_pos = [robot.move() for robot in robots]
        num_of_col_by_row = defaultdict(int)

        for cur_pos in new_pos:
            col_by_row[cur_pos.row].add(cur_pos.col)

            streak = 0
            streak_count = 0
            prev_num = None
            # Find rows with consecutive drones
            for cur_num in sorted(col_by_row[cur_pos.row]):
               if prev_num is None:
                   prev_num = cur_num
               elif cur_num != prev_num + 1:
                   if streak == 15:
                       streak_count += 1
                       if streak_count == 1:
                           found = True
                           break
                       print('counter', counter)
                       for row in range(total_rows):
                           for col in range(total_cols):
                               print('#' if col in col_by_row[row] else '.', end='')
                           print('')
                       print('')
                       print('/////////////////////////////////////')
                   streak = 0
               else:
                   pass

               prev_num = cur_num
               streak += 1

            # match len(col_by_row[cur_pos.row]):
            #     case 0:
            #         # found = False
            #         pass
            #     case 1:
            #         # found = False
            #         pass
            #     # case 2:
            #     #     # found &= abs(col_by_row[cur_pos.row][0] - Y_AXIS_COL) == abs(col_by_row[cur_pos.row][1] - Y_AXIS_COL)
            #     #     # found = False
            #     #     pass
            #     case 2:
            #         # print('4')
            #         prev_num = None
            #         # found = True
            #         # print(sorted(col_by_row[cur_pos.row]))
            #         for cur_num in sorted(col_by_row[cur_pos.row]):
            #             if prev_num is None:
            #                 prev_num = cur_num
            #
            #                 continue
            #             if cur_num != prev_num + 1:
            #                 break
            #         else:
            #             found = True
            #
            #
            #     case _:
            #         found = False
        # for temp_row in col_by_row.keys():
        #     num_of_col_by_row[len(col_by_row[temp_row])] += 1
        #
        # if len(num_of_col_by_row) < max_len_num_of_col_by_row:
        #     max_len_num_of_col_by_row = len(num_of_col_by_row)
        #     print('new max len', max_len_num_of_col_by_row)
        # if num_of_col_by_row[2] >= 25:
        #     pprint.pprint(num_of_col_by_row)
        #     found = True


    for row in range(total_rows):
        for col in range(total_cols):
            print('#' if col in col_by_row[row] else '.', end='')
        print('')
    print('')
    print('/////////////////////////////////////')
    print('b:', counter)
