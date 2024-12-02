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
# INPUT_FILE='2b-example.txt'

input = [[int(x) for x in line.split(' ')] for line in get_file_contents(INPUT_FILE)[0]]

def check_report(report: list[int], *, bad_level_allowed=False):
    res = check_report_helper(report)

    if res:
        return True

    # See if removing any element fixes
    if bad_level_allowed:
        for i in range(len(report)):
            copy_report = report.copy()
            del copy_report[i]
            res = check_report_helper(copy_report)
            if res:
                return True

    return False

def check_report_helper(report: list[int]):
    """Return true iif the report is valid"""
    diff = report[1] - report[0]
    # print('called with', report)

    if diff == 0:
        # Try the last few element
        diff = report[-1] - report[-2]
        if diff == 0:
            return False

    if diff > 0:
        mode = True  # Pos
    else:
        mode = False  # Neg

    for i in range(len(report)-1):
        bad_level = False
        cur_diff = report[i+1] - report[i]
        # print('i:', i, report[i], end='')

        if cur_diff == 0:
            bad_level = True
        elif mode:
            if cur_diff > 3 or cur_diff < 0:
                bad_level = True
        else:
            if cur_diff < -3 or cur_diff > 0:
                bad_level = True

        if bad_level:
            return False

        # print()
    # print()
    # print('return true')
    return True

def check_report2(report: list[int], *, num_bad_level_allowed=0):
    """
    Return true iif the report is valid

    More optimized version
    """
    diff = report[1] - report[0]
    # print('called with', report)
    if diff == 0:
        # Try the last few element
        diff = report[-1] - report[-2]
        if diff == 0:
            return False
    if diff > 0:
        mode = True  # Pos
    else:
        mode = False  # Neg
    for i in range(len(report)-1):
        bad_level = False
        cur_diff = report[i+1] - report[i]
        # print('i:', i, report[i], end='')

        if cur_diff == 0:
            bad_level = True
        elif mode:
            if cur_diff > 3 or cur_diff < 0:
                bad_level = True
        else:
            if cur_diff < -3 or cur_diff > 0:
                bad_level = True
        if bad_level:
            if num_bad_level_allowed == 0:
                return False
            else:
                copy_list = report.copy()
                del copy_list[i]
                # print()
                # print()
                res_remove_el = check_report(copy_list, num_bad_level_allowed=num_bad_level_allowed-1)

                if res_remove_el:
                    return True
                else:
                    copy_list = report.copy()
                    if i == 1:
                        idx_to_remove = 0
                    else:
                        idx_to_remove = i + 1
                    del copy_list[i + 1]
                    # print()
                    # print()
                    res_remove_el = check_report(copy_list, num_bad_level_allowed=num_bad_level_allowed-1)
                    if res_remove_el:
                        return True
                    if i == 1:
                        copy_list = report.copy()
                        del copy_list[0]
                        return check_report(copy_list, num_bad_level_allowed=num_bad_level_allowed-1)
                    return False

    #     print()
    # print()
    # print('return true')
    return True

print('a:', sum([check_report(x, num_bad_level_allowed=0) for x in input]))
# input = input[:]
# pprint.pprint([(x, check_report(x, num_bad_level_allowed=1)) for x in input])
# pprint.pprint([x for x in input if check_report(x, num_bad_level_allowed=1) is False])
print('b:', sum([check_report(x, num_bad_level_allowed=1) for x in input]))
