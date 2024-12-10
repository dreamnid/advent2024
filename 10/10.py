#!/usr/bin/env python3

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='10-input.txt'
# INPUT_FILE='10a-example.txt'
# INPUT_FILE='10a2-example.txt'
# INPUT_FILE='10a3-example.txt'
# INPUT_FILE='10b1-example.txt'
# INPUT_FILE='10b2-example.txt'

input = add_padding([[int(col) if col != '.' else None for col in line] for line in get_file_contents(INPUT_FILE)[0]])

def find_score(input, row_i: int, col_i: int, cur_step=0, visited=None, shared_visited=False):
    if visited is None:
        visited = set()
    visited.add((row_i, col_i))

    if input[row_i][col_i] == 9:
        # We reached the peak of the trail so this is a valid trail
        # pprint.pprint(visited)
        return 1

    if not shared_visited:
        visited = visited.copy()

    res = 0
    if input[row_i][col_i + 1] == cur_step + 1 and (row_i, col_i + 1) not in visited:
        res += find_score(input, row_i, col_i + 1, cur_step + 1, visited, shared_visited=shared_visited)
    if input[row_i+1][col_i] == cur_step + 1 and (row_i+1, col_i) not in visited:
        res += find_score(input, row_i + 1, col_i, cur_step + 1, visited, shared_visited=shared_visited)
    if input[row_i][col_i-1] == cur_step + 1 and (row_i, col_i-1) not in visited:
        res += find_score(input, row_i, col_i - 1, cur_step + 1, visited, shared_visited=shared_visited)
    if input[row_i-1][col_i] == cur_step + 1 and (row_i-1, col_i) not in visited:
        res += find_score(input, row_i - 1, col_i, cur_step + 1, visited, shared_visited=shared_visited)

    return res

res: list[int] = []
# pprint.pprint(input)

with PrintTiming('a'):
    for row_i, row in enumerate(input):
        for col_i, col in enumerate(row):
            if col == 0:
                # This is a potential trailhead
                if (score := find_score(input, row_i, col_i, shared_visited=True)):
                    res.append(score)

print('a:', sum(res))

res2: list[int] = []
with PrintTiming('a'):
    for row_i, row in enumerate(input):
        for col_i, col in enumerate(row):
            if col == 0:
                # This is a potential trailhead
                if (score := find_score(input, row_i, col_i, shared_visited=False)):
                    res2.append(score)
print('b:', sum(res2))
