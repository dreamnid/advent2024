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

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='5-input.txt'
# INPUT_FILE='5a-example.txt'

rules = [[int(char) for char in line.split('|')] for line in get_file_contents(INPUT_FILE)[0]]
updates = [[int(char) for char in line.split(',')] for line in get_file_contents(INPUT_FILE)[1]]

def check_rules(pages: list[int]):
    for rule in rules:
        try:
            first_pos = pages.index(rule[0])
            last_pos = pages.index(rule[1])
            if first_pos > last_pos:
                return False
        except ValueError:
            pass
    return True


def get_middle_el(my_list: list):
    idx = (len(my_list) - 1)//2
    return my_list[idx]


correct_updates: list[list[int]] = []
wrong_updates: list[list[int]] = []
for update in updates:
    if check_rules(update):
        correct_updates.append(update)
    else:
        wrong_updates.append(update)

with PrintTiming('a'):
    print('a:', sum(map(get_middle_el, correct_updates)))

before_map: dict[int, set[int]] = defaultdict(set)
"""the children must appear before the key"""
after_map: dict[int, set[int]] = defaultdict(set)
"""the children must appear after the key"""
for rule in rules:
    after_map[rule[0]].add(rule[1])
    before_map[rule[1]].add(rule[0])

# print('after', after_map)
# print('before', before_map)

def fix_pages(pages: list[int]):
    changed = True
    while changed:
        changed = False

        for rule in rules:
            try:
                # print(rule)
                first_pos = pages.index(rule[0])
                last_pos = pages.index(rule[1])
                if first_pos > last_pos:
                    # print('old', pages)
                    del pages[first_pos]
                    pages.insert(last_pos, rule[0])
                    # print('new', pages)
                    changed = True

            except ValueError:
                pass

# print(wrong_updates)
for update in wrong_updates:
    fix_pages(update)
    # break
# fix_pages(wrong_updates[2])

#o print(wrong_updates)
with PrintTiming('b'):
    print('b:', sum(map(get_middle_el, wrong_updates)))
