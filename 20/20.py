#!/usr/bin/env python3
import heapq
import pprint
from collections import Counter, defaultdict, deque
from copy import deepcopy
from enum import IntEnum
from typing import NamedTuple, TypeVar

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='20-input.txt'
# INPUT_FILE='20a-example.txt'

class Dir(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class Pos(NamedTuple):
    row: int
    col: int


def get_neighbors(input, pos: Pos):
    res = []

    if input[pos.row-1][pos.col] != '#':
        res.append((Pos(pos.row-1, pos.col)))
    if input[pos.row][pos.col+1] != '#':
        res.append((Pos(pos.row, pos.col+1)))
    if input[pos.row+1][pos.col] != '#':
        res.append((Pos(pos.row+1, pos.col)))
    if input[pos.row][pos.col-1] != '#':
        res.append((Pos(pos.row, pos.col-1)))

    return res

def get_wall_neighbors(input, pos: Pos):
    res = []

    if input[pos.row-1][pos.col] == '#':
        res.append((Pos(pos.row-1, pos.col), Dir.UP))
    if input[pos.row][pos.col+1] == '#':
        res.append((Pos(pos.row, pos.col+1), Dir.RIGHT))
    if input[pos.row+1][pos.col] == '#':
        res.append((Pos(pos.row+1, pos.col), Dir.DOWN))
    if input[pos.row][pos.col-1] == '#':
        res.append((Pos(pos.row, pos.col-1), Dir.LEFT))
    return res


T = TypeVar('T')


class PriorityQueue:
    def __init__(self):
        self.buffer: list[tuple[float, T]] = []

    def put(self, item: T, priority=0):
        heapq.heappush(self.buffer, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.buffer)[1]

    def __sizeof__(self):
        return len(self.buffer)


def manhattan_distance(a: Pos, b: Pos):
    return abs(a.row-b.row) + abs(a.col-b.col)


def a_star(input, start: Pos, end: Pos):
    myqueue = PriorityQueue()
    myqueue.put(start, 0)

    # Based on https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-astar

    came_from: dict[Pos, Pos | None] = {}
    cost: dict[Pos, int] = {}
    came_from[start] = None
    cost[start] = 0

    while myqueue:
        current_pos: Pos = myqueue.get()

        if current_pos == end:
            break

        for next in get_neighbors(input, current_pos):
            new_cost = cost[current_pos] + 1
            if next not in cost or new_cost < cost[next]:
                cost[next] = new_cost
                priority = new_cost + manhattan_distance(next, end)
                myqueue.put(next, priority)
                came_from[next] = current_pos

    return came_from, cost

input = add_padding([[cur_char for cur_char in line] for line in get_file_contents(INPUT_FILE)[0]], '#')

start_pos = None
end_pos = None
for row_i, row in enumerate(input):
    for col_i, col in enumerate(row):
        if col == 'S':
            start_pos = Pos(row_i, col_i)
        if col == 'E':
            end_pos = Pos(row_i, col_i)

        if start_pos and end_pos:
            break
    if start_pos and end_pos:
        break

class Axis(IntEnum):
    X = 0
    Y = 1

savings = defaultdict(int)
with PrintTiming('a'):
    new_path_nodes, cost = a_star(input, start_pos, end_pos)
    original_cost = len(new_path_nodes) - 1
    print(cost[end_pos])
    walls_tried = set()

    for node in new_path_nodes.keys():
        walls = get_wall_neighbors(input, node)
        next_walls_to_try = []
        for wall, dir in walls:
            match dir:
                case Dir.UP:
                    if input[wall.row-1][wall.col] != '#' and (wall, Axis.Y) not in walls_tried:
                        next_walls_to_try.append((wall, Pos(wall.row-1, wall.col)))
                        walls_tried.add((wall, Axis.Y))
                case Dir.RIGHT:
                    if input[wall.row][wall.col+1] != '#' and (wall, Axis.X) not in walls_tried:
                        next_walls_to_try.append((wall, Pos(wall.row, wall.col+1)))
                    walls_tried.add((wall, Axis.X))
                case Dir.DOWN:
                    if input[wall.row+1][wall.col] != '#' and (wall, Axis.Y) not in walls_tried:
                        next_walls_to_try.append((wall, Pos(wall.row+1, wall.col)))
                        walls_tried.add((wall, Axis.Y))
                case Dir.LEFT:
                    if input[wall.row][wall.col-1] != '#' and (wall, Axis.X) not in walls_tried:
                        next_walls_to_try.append((wall, Pos(wall.row, wall.col-1)))
                        walls_tried.add((wall, Axis.X))

        for next_wall, next_track in next_walls_to_try:
            if next_track in cost:
                # print(next_wall, 'cached')
                savings[cost[next_track] - cost[node] - 2] += 1
            else:
                # print(next_wall, 'not cached')

                new_input = deepcopy(input)
                new_input[next_wall.row][next_wall.col] = '.'

                new_path_nodes, new_cost = a_star(new_input, start_pos, end_pos)
                new_len = new_cost[end_pos]
                savings[original_cost - new_len] += 1

# pprint.pprint(savings)
print('a', sum([num for saving, num in savings.items() if saving >= 100]))
