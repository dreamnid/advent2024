#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from enum import IntEnum
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

INPUT_FILE='17-input.txt'
# INPUT_FILE='17a-example.txt'

input_contents = get_file_contents(INPUT_FILE)


registers: list[int] = []
for line in input_contents[0]:
    line_split = line.split(': ')
    registers.append(int(line_split[1]))


program = [int(x) for x in input_contents[1][0].split(': ')[1].split(',')]


class OpCode(IntEnum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7

def get_combo_operand(val):
    match val:
        case 0 | 1 | 2 | 3:
            return val
        case 4:
            return registers[0]
        case 5:
            return registers[1]
        case 6:
            return registers[2]
        case 7:
            raise ValueError()

ip = 0
out = []
while ip < len(program):
    cur_op = program[ip]
    operand = program[ip+1]
    jump = False

    match cur_op:
        case OpCode.adv:
            registers[0] //= 2 ** get_combo_operand(operand)
        case OpCode.bxl:
            registers[1] ^= operand
        case OpCode.bst:
            registers[1] = get_combo_operand(operand) % 8
        case OpCode.jnz:
            if registers[0] != 0:
                jump = True
                ip = operand
        case OpCode.bxc:
            registers[1] ^= registers[2]
        case OpCode.out:
            out.append(get_combo_operand(operand) % 8)
        case OpCode.bdv:
            registers[1] = registers[0] // 2 ** get_combo_operand(operand)
        case OpCode.cdv:
            registers[2] = registers[0] // 2 ** get_combo_operand(operand)
        case _:
            raise ValueError('Unknown opcode')

    if not jump:
        ip += 2

print('a:', ','.join(str(x) for x in out))
