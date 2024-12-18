#!/usr/bin/env python3
import heapq
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from enum import IntEnum
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul, ge, gt, itemgetter, le, lt, attrgetter
import os
import pprint
import re
from time import time
from typing import NamedTuple, TypeVar

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

INPUT_FILE='18-input.txt'
size = 71
first_bytes = 1024
# INPUT_FILE='18a-example.txt'
# size = 7
# first_bytes = 12

class Pos(NamedTuple):
    row: int
    col: int


input = list()
for line in get_file_contents(INPUT_FILE)[0]:
    line_split = line.split(',')

    input.append(Pos(int(line_split[1]), int(line_split[0])))

# pprint.pprint(input)

matrix = []
for row_i in range(size):
    row = []
    for col_i in range(size):
        if Pos(row_i, col_i) in input:
            char_to_add = '#'
        else:
            char_to_add = '.'
        row.append(char_to_add)
        # print(char_to_add, end='')
    matrix.append(row)
    # print()
matrix = add_padding(matrix, '#')


def print_matrix(matrix, path=None):
    if path is None:
        path = set()
    for row_i, row in enumerate(matrix):
        for col_i, char in enumerate(row):
            char_to_print = 'o' if Pos(row_i, col_i) in path else char
            print(char_to_print, end='')
        print()
    print()


def get_neighbors(input, pos: Pos):
    res = []

    if pos.row > 0 and Pos(pos.row-1, pos.col) not in input:
        res.append(Pos(pos.row-1, pos.col))
    if pos.col < size - 1 and Pos(pos.row, pos.col+1) not in input:
        res.append(Pos(pos.row, pos.col+1))
    if pos.row < size - 1 and Pos(pos.row+1, pos.col) not in input:
        res.append(Pos(pos.row+1, pos.col))
    if pos.col > 0 and Pos(pos.row, pos.col-1) not in input:
        res.append(Pos(pos.row, pos.col-1))
    return res


def manhattan_distance(a: Pos, b: Pos):
    return abs(a.row-b.row) + abs(a.col-b.col)


T = TypeVar('T')

class PriorityQueue:
    def __init__(self):
        self.buffer: list[tuple[float, T]] = []

    def put(self, item: T, priority=0):
        heapq.heappush(self.buffer, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.buffer)[1]

    def __sizeof__(self):
        return len(self.buffer)


def a_star(input, start: Pos, end: Pos):
    myqueue = PriorityQueue()
    myqueue.put(start, 0)

    # Based on https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-astar

    came_from: dict[Pos, Pos | None] = {}
    cost: dict[Pos, int] = {}
    came_from[start] = None
    cost[start] = 0

    while myqueue:
        current_pos: Pos = myqueue.get()

        if current_pos == end:
            break

        for next in get_neighbors(input, current_pos):
            new_cost = cost[current_pos] + 1
            if next not in cost or new_cost < cost[next]:
                cost[next] = new_cost
                priority = new_cost + manhattan_distance(next, end)
                myqueue.put(next, priority)
                came_from[next] = current_pos

    return came_from, cost


with PrintTiming('a'):
    _, cost = a_star(input[:first_bytes], Pos(0, 0), Pos(size-1, size-1))

print('a:', cost[Pos(size-1, size-1)])

with PrintTiming('b'):
    try:
        real_input = set(input[:first_bytes])
        for cur_first_bytes in range(first_bytes + 1, len(input)):
            _, cost = a_star(real_input, Pos(0, 0), Pos(size-1, size-1))
    except:
        pass
    block_y, block_x = input[cur_first_bytes - 1]

print(f'b: {block_x},{block_y}')
