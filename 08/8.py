#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from functools import partial, reduce
from itertools import chain, combinations, cycle, takewhile
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

INPUT_FILE='8-input.txt'
# INPUT_FILE='8a-example.txt'
# INPUT_FILE='8a2-example.txt'
# INPUT_FILE='8a3-example.txt'
# INPUT_FILE='8a4-example.txt'

file_contents = get_file_contents(INPUT_FILE)[0]
height = len(file_contents)
width = len(file_contents[0])
input = {row_i: {col_i: col for col_i, col in enumerate(line)} for row_i, line in enumerate(file_contents)}

Point = tuple[int, int]

nodes = defaultdict(list)

for i in range(height):
    for j in range(width):
        match input[i][j]:
            case '.':
                pass
            case _:
                nodes[input[i][j]].append((i, j))


def get_dist(point1: Point, point2: Point):
    return point2[0] - point1[0], point2[1] - point1[1]


def has_antinodes(point1: Point, point2: Point):
    dist = get_dist(point1, point2)
    return abs(dist[0]) > 0 or abs(dist[1]) > 0


antinode_positions = defaultdict(list)
unique_global_antinode_positions = set()
antinode_count = 0
for val, positions in nodes.items():
    for pos1, pos2 in combinations(positions, 2):
        if has_antinodes(pos1, pos2):
            # print(pos1, pos2, f' create anti nodes')
            dist = get_dist(pos1, pos2)
            cur_pos = pos1[0] - dist[0], pos1[1] - dist[1]
            if cur_pos[0] >= 0 and cur_pos[0] < height and cur_pos[1] >= 0 and cur_pos[1] < width:
                # print('add antinode', cur_pos)
                antinode_positions[val].append(cur_pos)
                unique_global_antinode_positions.add(cur_pos)

            cur_pos = pos2[0] + dist[0], pos2[1] + dist[1]
            if cur_pos[0] >= 0 and cur_pos[0] < height and cur_pos[1] >= 0 and cur_pos[1] < width:
                # print('add antinode', cur_pos)
                antinode_positions[val].append(cur_pos)
                unique_global_antinode_positions.add(cur_pos)
print('a:', len(unique_global_antinode_positions))
# pprint.pprint(antinode_postions)
