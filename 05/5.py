#!/usr/bin/env python3

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

def fix_pages(pages: list[int]):
    changed = True
    while changed:
        changed = False

        for rule in rules:
            try:
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
