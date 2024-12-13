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

INPUT_FILE='13-input.txt'
# INPUT_FILE='13a-example.txt'

file_contents = get_file_contents(INPUT_FILE)
movement_re = re.compile(r'X([+-]\d+), Y([+-]\d+)')
prize_re = re.compile(r'Prize: X=(\d+), Y=(\d+)')

with PrintTiming('a'):
    coins = []
    for machine_num in range(len(file_contents)):
        input = [line for line in get_file_contents(INPUT_FILE)[machine_num]]
        button_a_re = movement_re.search(input[0])
        button_a_move = int(button_a_re.group(1)), int(button_a_re.group(2))
        button_b_re = movement_re.search(input[1])
        button_b_move = int(button_b_re.group(1)), int(button_b_re.group(2))
        prize_coord = tuple(int(j) for j in prize_re.findall(input[2])[0])

        i = 0
        done = False
        while True:
            j = 0
            while True:
                x = button_a_move[0] * i
                y = button_a_move[1] * i
                x += button_b_move[0] * j
                y += button_b_move[1] * j

                if x == prize_coord[0] and y == prize_coord[1]:
                    done = True
                    break
                elif x > prize_coord[0] or y > prize_coord[1]:
                    break
                j += 1
            if done:
                break
            if i > 100 or button_a_move[0] * i > prize_coord[0] or button_a_move[1] * i > prize_coord[1]:
                break
            i += 1

        if done:
            coins.append(i*3 + j)
            # print('a count', i)
            # print('b count', j)

print('a', sum(coins))
