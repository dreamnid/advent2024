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

class Data(NamedTuple):
    nodes: set[str]
    last_node_added: str

with PrintTiming('A'):
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
print('a', sum(any(j.startswith('t') for j in i) for i in interconnected if len(i) == 3))

N = neighbors


def BronKerbosch1(P, R: set | None = None, X: set |None = None):
    """
    Use the Bron Kerbosch algorithm to find the cliques that are connected

    https://stackoverflow.com/a/59339555
    """
    P = set(P)
    R = set() if R is None else R
    X = set() if X is None else X
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        yield from BronKerbosch1(
            P=P.intersection(N[v]), R=R.union([v]), X=X.intersection(N[v]))
        X.add(v)


with PrintTiming('b'):
    max_interconnected_size = 0
    max_interconnected_nodes = None
    for cur_interconnected in BronKerbosch1(neighbors.keys()):
        if len(cur_interconnected) > max_interconnected_size:
            max_interconnected_size = len(cur_interconnected)
            max_interconnected_nodes = cur_interconnected

print('b', ','.join(sorted(list(max_interconnected_nodes))))
