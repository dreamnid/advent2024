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

INPUT_FILE='24-input.txt'
# INPUT_FILE='24a-example.txt'
# INPUT_FILE='24a2-example.txt'

file_contents = get_file_contents((INPUT_FILE))
input = [line for line in file_contents[0]]

def gate_value(gate, left, right):
    res = None
    match gate:
        case 'AND':
            res = left and right
        case 'OR':
            res = left or right
        case 'XOR':
            res = left ^ right
    return res

wire_value = dict()
for line in input:
    line_split = line.split(': ')
    wire_value[line_split[0]] = int(line_split[1] == '1')

gate_regex = re.compile(r'(\w+) (\w+) (\w+) -> (\w+)')
next_wire_value = wire_value.copy()
queued = deque()


for line in file_contents[1]:
    matches = gate_regex.match(line)

    try:
        next_wire_value[matches.group(4)] = gate_value(matches.group(2), wire_value[matches.group(1)], wire_value[matches.group(3)])

        wire_value = next_wire_value
    except KeyError:
        queued.append((matches.group(2), matches.group(1), matches.group(3), matches.group(4)))

while queued:
    attempt = queued.popleft()
    try:
        next_wire_value[attempt[3]] = gate_value(attempt[0], wire_value[attempt[1]], wire_value[attempt[2]])
    except KeyError:
        queued.append(attempt)

# Convert the zXX values to decimal, z_0 is the LSB
res = []
z_i = 0
while True:
    key = f'z{z_i:02d}'
    if key in wire_value:
        res.append(str(next_wire_value[key]))
    else:
        break
    z_i += 1
final_res = int(''.join(reversed(res)), 2)
print('a', final_res)

print(f'{final_res:b}')
