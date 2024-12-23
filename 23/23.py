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

INPUT_FILE='23-input.txt'
# INPUT_FILE='23a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

neighbors = defaultdict(list)
for line in input:
    line_split = line.split('-')
    neighbors[line_split[0]].append(line_split[1])
    neighbors[line_split[0]].sort()
    neighbors[line_split[1]].append(line_split[0])
    neighbors[line_split[1]].sort()
# pprint.pprint(neighbors)

interconnected = set()
for node, cur_neighbors in neighbors.items():
    for second_neighbor in cur_neighbors:
        if second_neighbor == node:
            continue
        for third_neighbor in neighbors[second_neighbor]:
            if third_neighbor == node:
                continue
            if node in neighbors[third_neighbor]:
                key = tuple(sorted([node, second_neighbor, third_neighbor]))
                interconnected.add(key)
# pprint.pprint(interconnected)
print('a', sum(any(j.startswith('t') for j in i) for i in interconnected))

