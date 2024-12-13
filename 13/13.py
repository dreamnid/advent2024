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
# INPUT_FILE='13b1-example.txt'

file_contents = get_file_contents(INPUT_FILE)
movement_re = re.compile(r'X([+-]\d+), Y([+-]\d+)')
prize_re = re.compile(r'Prize: X=(\d+), Y=(\d+)')

def solver(button_a_move, button_b_move, prize_coord):
    i = 0
    done = False
    while True:
        j = (prize_coord[0] - (button_a_move[0] * i)) / button_b_move[0]
        if j.is_integer():
            x = button_a_move[0] * i
            y = button_a_move[1] * i
            x += button_b_move[0] * j
            y += button_b_move[1] * j

            if x == prize_coord[0] and y == prize_coord[1]:
                done = True
                break
        if done:
            break
        if button_a_move[0] * i > prize_coord[0] or button_a_move[1] * i > prize_coord[1]:
            break
        i += 1

    if done:
        print('a count', i)
        print('b count', j)
        return i * 3 + j
    return 0


def solver2(button_a_move, button_b_move, prize_coord):
    # Solve for 2 unknowns with 2 equations
    multiplier = -button_a_move[0] / button_a_move[1]
    # print('multiplier', multiplier)

    # Figure new y multiplier
    temp = button_b_move[0] + (button_b_move[1] * multiplier)
    # Add third term
    temp2 = prize_coord[0] + (prize_coord[1] * multiplier)

    b_count = round(temp2/temp)
    a_count = round((prize_coord[0] - (button_b_move[0] * b_count))/button_a_move[0])
    # print('a_count', a_count)
    temp_a = button_a_move[0] * a_count + button_b_move[0] * b_count
    temp_b = button_a_move[1] * a_count + button_b_move[1] * b_count
    # print('temp_a', temp_a, prize_coord[0], temp_a == prize_coord[0], 'temp_b', temp_b,
          # prize_coord[1], temp_b == prize_coord[1])
    if temp_a == prize_coord[0] and temp_b == prize_coord[1]:
        return a_count * 3 + b_count

    # print(button_a_move[0] + (button_b_move[0] * multiplier), temp2, temp2/temp, math.isclose(int(res), res))

    #     if x == prize_coord[0] and y == prize_coord[1]:
    #         done = True
    # if done:
    #     print('a count', i)
    #     print('b count', j)
    #     return i * 3 + j
    return 0

def solver_numpy(button_a_move, button_b_move, prize_coord):
    a = np.array([[button_a_move[0], button_b_move[0]], [button_a_move[1], button_b_move[1]]])
    b = np.array([prize_coord[0], prize_coord[1]])
    x = np.linalg.solve(a, b)
    a_count = int(x[0])
    b_count = int(x[1])
    temp_a = button_a_move[0] * a_count + button_b_move[0] * b_count
    temp_b = button_a_move[1] * a_count + button_b_move[1] * b_count

    # print('temp_a', temp_a, prize_coord[0], temp_a == prize_coord[0], 'temp_b', temp_b,
    #       prize_coord[1], temp_b == prize_coord[1])
    if temp_a == prize_coord[0] and temp_b == prize_coord[1]:
        return a_count * 3 + b_count
    return 0


with PrintTiming('a'):
    coins = []
    for machine_num in range(len(file_contents)):
        input = [line for line in get_file_contents(INPUT_FILE)[machine_num]]
        button_a_re = movement_re.search(input[0])
        button_a_move = int(button_a_re.group(1)), int(button_a_re.group(2))
        button_b_re = movement_re.search(input[1])
        button_b_move = int(button_b_re.group(1)), int(button_b_re.group(2))
        prize_coord = tuple(int(j) for j in prize_re.findall(input[2])[0])
        coins.append(solver2(button_a_move, button_b_move, prize_coord))
    print('a', sum(coins))

with PrintTiming('b'):
    coins = []
    for machine_num in range(len(file_contents)):
        input = [line for line in get_file_contents(INPUT_FILE)[machine_num]]
        button_a_re = movement_re.search(input[0])
        button_a_move = int(button_a_re.group(1)), int(button_a_re.group(2))
        button_b_re = movement_re.search(input[1])
        button_b_move = int(button_b_re.group(1)), int(button_b_re.group(2))
        prize_coord = tuple(int(j) + 10000000000000 for j in prize_re.findall(input[2])[0])
        coins.append(solver2(button_a_move, button_b_move, prize_coord))

    print('b', sum(coins))
