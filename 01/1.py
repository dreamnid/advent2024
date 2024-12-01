#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul, ge, gt, itemgetter, le, lt, sub
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

INPUT_FILE='1-input.txt'
# INPUT_FILE='1a-example.txt'

input = [line.split('   ') for line in get_file_contents(INPUT_FILE)[0]]
transpose_input = [[int(input[j][i]) for j in range(len(input))] for i in range(len(input[0]))]
sorted_transpose_input = sorted(transpose_input[0]), sorted(transpose_input[1])

a = reduce(lambda a, x: a + abs(x[1]-x[0]), zip(sorted_transpose_input[0], sorted_transpose_input[1]), 0)
print('part a:', a)

c = Counter(transpose_input[1])
b = reduce(lambda a, x: a + x * c[x],transpose_input[0], 0)
print('part b:', b)
