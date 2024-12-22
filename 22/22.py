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

INPUT_FILE='22-input.txt'
INPUT_FILE='22a-example.txt'
INPUT_FILE='22b-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]


def prune(num):
    return num % 16777216


def next_secret(num):
    # print(f'{num:#026b}')
    num = prune((num << 6) ^ num)
    # print(f'{num:#026b}')
    num = prune((num >> 5) ^ num)
    # print(f'{num:#026b}')
    return prune((num << 11) ^ num)


# secret = 123
# for i in range(2000):
#     secret = next_secret(secret)
#     print(f'{secret:#026b} {secret}')
#     print('------'*10)
#     # print(i, secret)
# input = ['123']
new_secrets: list[int] = []
prices: list[list[int]] = []
price_changes: list[list[int]] = []
with PrintTiming('a'):
    for line in input:
        secret = int(line)
        cur_prices = [secret % 10]
        cur_price_changes = []
        cur_highest_price = 0
        for i in range(2000):
            secret = next_secret(secret)
            cur_price = secret % 10
            if cur_price > cur_highest_price:
                cur_highest_price = cur_price
            cur_price_changes.append(cur_price - cur_prices[-1])
            cur_prices.append(cur_price)
        new_secrets.append(secret)
        prices.append(cur_prices)
        price_changes.append(cur_price_changes)

print('a', sum(new_secrets))


pprint.pprint([[(prices[i][j], price_change) for j, price_change in enumerate(cur_price_changes)] for i, cur_price_changes in enumerate(price_changes)])
def find_change_idx(desired_seq: list[int], changes: list[int]):
    """Find price for the given change sequence"""
    seq_i = 0
    for i, change in enumerate(changes):
        if change == desired_seq[seq_i]:
            if seq_i == 3:
                return i
            seq_i += 1
        else:
            seq_i = 0
    return 0


monkey_bought_price: list[int] = []
for i in range(len(input)):
    change_idx = find_change_idx([-1,-1,0,2], price_changes[i])
    monkey_bought_price.append(prices[i][change_idx+1])

pprint.pprint(monkey_bought_price)
print('b:', sum(monkey_bought_price))
