#!/usr/bin/env python3
import copy
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

INPUT_FILE='15-input.txt'
# INPUT_FILE='15a-example.txt'
# INPUT_FILE='15a2-example.txt'
# INPUT_FILE='15b-example.txt'
# INPUT_FILE='15bgio1-example.txt'

input = [[char for char in line] for line in get_file_contents(INPUT_FILE)[0]]
input2 = copy.deepcopy(input)

# pprint.pprint(input2)

for row_i, row in enumerate(input):
    try:
        col_i = row.index('@')
        robot = orig_robot = (row_i, col_i)
        break
    except ValueError:
        pass

def get_movement_for_dir(dir: str):
    """Returns the number of rows and number of cols respectively"""
    match dir:
        case '^':
            return -1, 0
        case '>':
            return 0, 1
        case 'v':
            return 1, 0
        case '<':
            return 0, -1


def move_pos(input, old_pos, new_pos):
    input[new_pos[0]][new_pos[1]] = input[old_pos[0]][old_pos[1]]
    input[old_pos[0]][old_pos[1]] = '.'


def move_pos2(input, pos_itr, movement):
    for cur_pos in pos_itr:
        input[cur_pos[0] + movement[0]][cur_pos[1] + movement[1]] = input[cur_pos[0]][cur_pos[1]]
        input[cur_pos[0]][cur_pos[1]] = '.'


directions = [char for line in get_file_contents(INPUT_FILE)[1] for char in line]

with PrintTiming('a'):
    for dir_i, dir in enumerate(directions):
        movement = get_movement_for_dir(dir)

        new_pos = robot[0] + movement[0], robot[1] + movement[1]
        match input[new_pos[0]][new_pos[1]]:
            case '.':
                move_pos(input, robot, new_pos)
                robot = new_pos
            case 'O':
                steps: list[tuple[tuple[int, int], tuple[int, int]]] = [(robot, new_pos)]
                cur_temp_pos = new_pos
                while True:
                    new_temp_pos = cur_temp_pos[0] + movement[0], cur_temp_pos[1] + movement[1]
                    steps.append((cur_temp_pos, new_temp_pos))
                    match input[new_temp_pos[0]][new_temp_pos[1]]:
                        case '.':
                            # Shift boxes
                            for cur_step in steps[::-1]:
                                move_pos(input, cur_step[0], cur_step[1])
                            robot = cur_step[1]
                            break
                        case 'O':
                            # Keep stepping
                            pass
                        case '#':
                            break
                    cur_temp_pos = new_temp_pos

        if dir_i % 10 == 0 and False:
            print(dir_i, dir)
            pprint.pprint(input)

    # pprint.pprint(input)
    # input = ['#######', '#...O..', '#......']

    res = [(row_i * 100 + col_i) for row_i, row in enumerate(input) for col_i, col in enumerate(row) if col == 'O']
print('a:', sum(res))


def expand(cur_char):
    match cur_char:
        case '#':
            return '##'
        case 'O':
            return '[]'
        case '.':
            return '..'
        case '@':
            return '@.'


def get_coords_for_mega_box(input, row, col):
    if input[row][col] == '[':
        start_col = col
    else:
        start_col = col - 1
    return ((row, start_col), (row, start_col + 1))


input2 = [[expand_char for char in row for expand_char in expand(char)] for row in input2]
robot2 = orig_robot[0], orig_robot[1] * 2
# pprint.pprint(input2, width=120)

with PrintTiming('b'):
    for dir_i, dir in enumerate(directions):
        movement = get_movement_for_dir(dir)

        new_pos = robot2[0] + movement[0], robot2[1] + movement[1]
        match input2[new_pos[0]][new_pos[1]]:
            case '.':
                move_pos(input2, robot2, new_pos)
                robot2 = new_pos
            case '[' | ']':
                steps: list[tuple[tuple[int, int], tuple[int, int]]] = [(robot2,)]

                # if dir in ['v', '^']:
                #     if input2[new_pos[0]][new_pos[1]] == '[':
                #         steps.append(((new_pos[0], new_pos[1] + 1), (new_pos[0] + movement[0], new_pos[1] + 1)))
                #     else:
                #         steps.append(((new_pos[0], new_pos[1] - 1), (new_pos[0] + movement[0], new_pos[1] - 1)))
                if dir in ['v', '^']:
                    initial_box = get_coords_for_mega_box(input2, new_pos[0], new_pos[1])
                    boxes_to_move = [initial_box]
                    next_new_boxes = [initial_box]
                    blocked = False

                    while next_new_boxes and not blocked:
                        new_boxes = next_new_boxes
                        next_new_boxes = set()
                        for box in new_boxes:
                            # find what's above/below the box
                            match input2[box[0][0] + movement[0]][box[0][1] + movement[1]]:
                                case '[':
                                    next_new_boxes.add(((box[0][0] + movement[0], box[0][1]), (box[0][0] + movement[0], box[0][1] + 1)))
                                case ']':
                                    next_new_boxes.add(((box[0][0] + movement[0], box[0][1] - 1), (box[0][0] + movement[0], box[0][1])))
                                case '#':
                                    blocked = True
                                    break

                            # find what's above/below the box
                            match input2[box[1][0] + movement[0]][box[1][1] + movement[1]]:
                                case '[':
                                    next_new_boxes.add(((box[1][0] + movement[0], box[1][1]), (box[1][0] + movement[0], box[1][1] + 1)))
                                case '#':
                                    blocked = True
                                    break
                        boxes_to_move.extend(list(next_new_boxes))

                    if not blocked:
                        for cur_box in boxes_to_move[::-1]:
                            move_pos2(input2, cur_box, movement)
                        move_pos(input2, robot2, new_pos)
                        robot2 = new_pos
                else:
                    cur_temp_pos = new_pos
                    while True:
                        steps.append((cur_temp_pos,))

                        new_temp_pos = cur_temp_pos[0] + movement[0], cur_temp_pos[1] + movement[1]
                        match input2[new_temp_pos[0]][new_temp_pos[1]]:
                            case '.':
                                # Shift boxes
                                for cur_step in steps[::-1]:
                                    #move_pos(input2, cur_step[0], cur_step[1])
                                    move_pos2(input2, cur_step, movement)
                                robot2 = cur_step[0][0] + movement[0], cur_step[0][1] + movement[1]
                                break
                            case 'O':
                                pass
                            case '[' | ']':
                                pass
                            case '#':
                                break
                        cur_temp_pos = new_temp_pos

        # if dir_i % 10 == 0 or True:
        #     print(dir_i, dir)
        #     pprint.pprint(input2, width=120)
    res2 = [(row_i * 100 + col_i) for row_i, row in enumerate(input2) for col_i, col in enumerate(row) if col == '[']
# pprint.pprint(input2, width=510)
print('b:', sum(res2))
