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

# print(input)

# populate disk
disk = []
cur_id = 0
for i, cur_num in enumerate(input):
    if i % 2 == 0:
        disk.extend([cur_id] * cur_num)
        cur_id += 1
    else:
        disk.extend([None] * cur_num)
        pass

with PrintTiming('a'):
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
