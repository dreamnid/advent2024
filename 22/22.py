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

INPUT_FILE='22-input.txt'
# INPUT_FILE='22a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]


def prune(num):
    return num % 16777216


def next_secret(num):
    # print(f'{num:#026b}')
    num = prune((num << 6) ^ num)
    # print(f'{num:#026b}')
    num = prune((num >> 5) ^ num)
    # print(f'{num:#026b}')
    return prune((num << 11) ^ num)


# secret = 123
# for i in range(2000):
#     secret = next_secret(secret)
#     print(f'{secret:#026b} {secret}')
#     print('------'*10)
#     # print(i, secret)

with PrintTiming('a'):
    res = []
    for line in input:
        secret = int(line)
        for i in range(2000):
            secret = next_secret(secret)
        res.append(secret)

# pprint.pprint(res)
print('a', sum(res))
