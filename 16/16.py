#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from enum import StrEnum, IntEnum
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul, ge, gt, itemgetter, le, lt, attrgetter
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

INPUT_FILE='16-input.txt'
# INPUT_FILE='16a-example.txt'
# INPUT_FILE='16a2-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

class Dir(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class Pos(NamedTuple):
    row: int
    col: int


def get_next_movement(input, pos: Pos, prev_visit: set):
    res = []

    if input[pos.row-1][pos.col] != '#' and Pos(pos.row-1, pos.col) not in prev_visit:
        res.append((Pos(pos.row-1, pos.col), Dir.UP))
    if input[pos.row][pos.col+1] != '#' and Pos(pos.row, pos.col+1) not in prev_visit:
        res.append((Pos(pos.row, pos.col+1), Dir.RIGHT))
    if input[pos.row+1][pos.col] != '#' and Pos(pos.row+1, pos.col) not in prev_visit:
        res.append((Pos(pos.row+1, pos.col), Dir.DOWN))
    if input[pos.row][pos.col-1] != '#' and Pos(pos.row, pos.col-1) not in prev_visit:
        res.append((Pos(pos.row, pos.col-1), Dir.LEFT))
    return res


@dataclass
class Data:
    path: list
    visited: set
    cost: int
    last_dir: Dir | None = None


cur_pos: Pos | None = None
for row_i, row in enumerate(input):
    for col_i, col in enumerate(row):
        if col == 'S':
            cur_pos = Pos(row_i, col_i)
            break

with PrintTiming('a'):
    queue = [Data(path=[cur_pos], visited=set(), cost=0, last_dir=Dir.RIGHT)]
    lowest_cost_for_pos = dict()
    finished = []
    while queue:
        cur_data = queue.pop(0)
        cur_pos = cur_data.path[-1]
        if input[cur_pos.row][cur_pos.col] == 'E':
            finished.append(cur_data)
            # print('found with cost', cur_data.cost)
            continue

        cur_data.visited.add(cur_pos)
        next_moves = get_next_movement(input, cur_pos, cur_data.visited)

        copy_data = len(next_moves) > 1
        for next_move in next_moves:
            cost = cur_data.cost + 1
            if next_move[0].row == 7 and next_move[0].col == 15 and False:
                print(cost, lowest_cost_for_pos[next_move[0]] if next_move[0] in lowest_cost_for_pos else 'inf', cur_data.path)
            if next_move[0] not in lowest_cost_for_pos or (cost <= lowest_cost_for_pos[next_move[0]] + 1000):

                lowest_cost_for_pos[next_move[0]] = cost
                if cur_data.last_dir != next_move[1]:
                    if next_move[0].row == 6 and False:
                        print('add 1000', Dir(cur_data.last_dir), next_move)
                    cost += 1000
                    # print('before', Pos(cur_data.path[-1].row, cur_data.path[-1].col), lowest_cost_for_pos[Pos(cur_data.path[-1].row, cur_data.path[-1].col)] if Pos(cur_data.path[-1].row, cur_data.path[-1].col) in lowest_cost_for_pos else '#')
                    lowest_cost_for_pos[Pos(cur_data.path[-1].row, cur_data.path[-1].col)] = cost - 1
                    # print('after', Pos(cur_data.path[-1].row, cur_data.path[-1].col), lowest_cost_for_pos[Pos(cur_data.path[-1].row, cur_data.path[-1].col)])
                next_path = cur_data.path.copy() if copy_data else cur_data.path
                next_path.append(next_move[0])

                next_visited = cur_data.visited.copy() if copy_data else cur_data.visited
                queue.append(Data(path=next_path, visited=next_visited, cost=cost, last_dir=next_move[1]))

# pprint.pprint(sorted(finished, key=lambda x: x.cost)[0])
best_cost_data = sorted(finished, key=attrgetter('cost'))
print('a:', best_cost_data[0].cost, best_cost_data[1].cost)
# pprint.pprint(best_cost_data.path)

best_data = [data for data in best_cost_data if data.cost == best_cost_data[0].cost]
best_tiles = set()
for data in best_data:
    best_tiles.update(data.path)

# for row_i, row in enumerate(input):
#     for col_i, col in enumerate(row):
#         if col == '.':
#             print('O' if Pos(row_i, col_i) in best_tiles else '.', end='')
#         else:
#             print(col, end='')
#     print()

print('b:', len(best_tiles))
