#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from functools import partial, reduce
from itertools import accumulate, chain, cycle, takewhile
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

INPUT_FILE='2-input.txt'
# INPUT_FILE='2a-example.txt'

input = [[int(x) for x in line.split(' ')] for line in get_file_contents(INPUT_FILE)[0]]

def my_func(my_list: Sequence[int]):
    diff = my_list[1] - my_list[0]
    if diff == 0:
        return False
    if diff > 0:
        mode = 1  # Pos
    else:
        mode = 0  # Neg

    for i in range(len(my_list)-1):
        cur_diff = my_list[i+1] - my_list[i]
        if cur_diff == 0:
            return False
        if mode:
            if cur_diff > 3 or cur_diff < 0:
                return False
        else:
            if cur_diff < -3 or cur_diff > 0:
                return False
    return True

print('a: ', sum([my_func(x) for x in input]))