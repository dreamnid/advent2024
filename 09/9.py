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

INPUT_FILE='9-input.txt'
# INPUT_FILE='9a-example.txt'
# INPUT_FILE='9a2-example.txt'

input = [int(cur_char) for line in get_file_contents(INPUT_FILE)[0] for cur_char in line]


def get_continuous_size(block_id):
    cur_size = 0
    target_val = disk[block_id]
    for i in range(block_id, len(disk) - 1):
        if disk[i] == target_val:
            cur_size += 1
        else:
            break

    return cur_size

# print(input)

# populate disk
input_disk = []
cur_id = 0
cur_block = 0
file_size = {}
file_first_block = {}
files = []  # file id, size
temp_free_space = []  # blk id, space
free_space = []  # blk id, space

for i, cur_num in enumerate(input):
    if i % 2 == 0:
        input_disk.extend([cur_id] * cur_num)
        file_size[cur_id] = cur_num
        file_first_block[cur_id] = cur_block
        files.append((cur_id, cur_num))
        cur_id += 1
    else:
        if cur_num:
            input_disk.extend([None] * cur_num)
            temp_free_space.append((cur_block, cur_num))
            free_space.append((cur_block, cur_num))
    cur_block += cur_num

# for cur_blk_id, cur_free_space in temp_free_space:
#     if not free_space or (free_space and cur_blk_id > (free_space[-1][0] + free_space[-1][1])):
#         size = get_continuous_size(cur_blk_id)
#         free_space.append((cur_blk_id, size))
# print(disk)

with PrintTiming('a'):
    disk = input_disk.copy()
    for i, cur_num in enumerate(reversed(disk)):
        real_idx = len(disk) - 1 - i
        if cur_num is not None:
            try:
                first_space_idx = disk.index(None)
                disk[first_space_idx] = cur_num
                disk[real_idx] = None
            except ValueError:
                break
        # print(disk)
    # move free space from beginning to end
    for i in range(disk.index(0)):
        del disk[0]
        disk.append(None)

    chksum = [i * val for i, val in enumerate(disk) if val is not None]
print('a:', sum(chksum))

with PrintTiming('b'):
    disk = input_disk.copy()
    unmoved_files = list(reversed(files))
    for unmoved_file_id, cur_size in unmoved_files:
        for space_idx, (space_blk_id, space_size) in enumerate(free_space):
            if space_blk_id < file_first_block[unmoved_file_id] and cur_size <= space_size:
                for k in range(space_blk_id, space_blk_id + cur_size):
                    disk[k] = unmoved_file_id
                for k in range(file_first_block[unmoved_file_id], file_first_block[unmoved_file_id] + cur_size):
                    disk[k] = None

                if cur_size == space_size:
                    del free_space[space_idx]
                else:
                    # Calc new space left
                    free_space[space_idx] = (space_blk_id + cur_size, space_size - cur_size)
                break

        # print(disk)
        # print(free_space)
    # move free space from beginning to end
    # for i in range(disk.index(0)):
    #     del disk[0]
    #     disk.append(None)

    chksum = [i * val for i, val in enumerate(disk) if val is not None]
# print(disk)
print('b:', sum(chksum))
