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


def get_neighbors(input, pos: Pos, finish_pos=None):
    res = []

    if input[pos.row-1][pos.col] in ['.', 'E', 'S']:
        res.append((Pos(pos.row-1, pos.col)))
    if input[pos.row][pos.col+1] in ['.', 'E', 'S']:
        res.append((Pos(pos.row, pos.col+1)))
    if input[pos.row+1][pos.col] in ['.', 'E', 'S']:
        res.append((Pos(pos.row+1, pos.col)))
    if input[pos.row][pos.col-1] in ['.', 'E', 'S']:
        res.append((Pos(pos.row, pos.col-1)))

    return res

def get_wall_neighbors_with_dir(input, pos: Pos, finish_pos=None):
    res = []

    if input[pos.row-1][pos.col] == '#' or (finish_pos == Pos(pos.row-1, pos.col)):
        res.append((Pos(pos.row-1, pos.col), Dir.UP))
    if input[pos.row][pos.col+1] == '#' or (finish_pos == Pos(pos.row, pos.col+1)):
        res.append((Pos(pos.row, pos.col+1), Dir.RIGHT))
    if input[pos.row+1][pos.col] == '#' or (finish_pos == Pos(pos.row+1, pos.col)):
        res.append((Pos(pos.row+1, pos.col), Dir.DOWN))
    if input[pos.row][pos.col-1] == '#' or (finish_pos == Pos(pos.row, pos.col-1)):
        res.append((Pos(pos.row, pos.col-1), Dir.LEFT))
    return res


def get_cheat_neighbors(input, pos: Pos, finish_pos=None):
    res = []

    if input[pos.row-1][pos.col] != '/':
        res.append(Pos(pos.row-1, pos.col))
    if input[pos.row][pos.col+1] != '/':
        res.append(Pos(pos.row, pos.col+1))
    if input[pos.row+1][pos.col] != '/':
        res.append(Pos(pos.row+1, pos.col))
    if input[pos.row][pos.col-1] != '/':
        res.append(Pos(pos.row, pos.col-1))
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


def a_star(input, start: Pos, end: Pos, neighbors_func=get_neighbors):
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

        for next in neighbors_func(input, current_pos, end):
            new_cost = cost[current_pos] + 1
            if next not in cost or new_cost < cost[next]:
                cost[next] = new_cost
                priority = new_cost + manhattan_distance(next, end)
                myqueue.put(next, priority)
                came_from[next] = current_pos

    return came_from, cost

# Change border to another character
file_contents = get_file_contents(INPUT_FILE)[0]
file_contents[0] = '/' * len(file_contents[0])
file_contents[len(file_contents)-1] = '/' * len(file_contents[0])

input = [['/' if i == 0 or i == len(file_contents[0]) - 1 else cur_char for i, cur_char in enumerate(line)] for line in file_contents]
# pprint.pprint(input)


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
# with PrintTiming('a'):
#     new_path_nodes, cost = a_star(input, start_pos, end_pos)
#     original_cost = len(new_path_nodes) - 1
#     print(cost[end_pos])
#     walls_tried = set()
#
#     for node in new_path_nodes.keys():
#         walls = get_wall_neighbors_with_dir(input, node)
#         next_walls_to_try = []
#         for wall, dir in walls:
#             match dir:
#                 case Dir.UP:
#                     if input[wall.row-1][wall.col] != '#' and (wall, Axis.Y) not in walls_tried:
#                         next_walls_to_try.append((wall, Pos(wall.row-1, wall.col)))
#                         walls_tried.add((wall, Axis.Y))
#                 case Dir.RIGHT:
#                     if input[wall.row][wall.col+1] != '#' and (wall, Axis.X) not in walls_tried:
#                         next_walls_to_try.append((wall, Pos(wall.row, wall.col+1)))
#                     walls_tried.add((wall, Axis.X))
#                 case Dir.DOWN:
#                     if input[wall.row+1][wall.col] != '#' and (wall, Axis.Y) not in walls_tried:
#                         next_walls_to_try.append((wall, Pos(wall.row+1, wall.col)))
#                         walls_tried.add((wall, Axis.Y))
#                 case Dir.LEFT:
#                     if input[wall.row][wall.col-1] != '#' and (wall, Axis.X) not in walls_tried:
#                         next_walls_to_try.append((wall, Pos(wall.row, wall.col-1)))
#                         walls_tried.add((wall, Axis.X))
#
#         for next_wall, next_track in next_walls_to_try:
#             if next_track in cost:
#                 # print(next_wall, 'cached')
#                 savings[cost[next_track] - cost[node] - 2] += 1
#             else:
#                 # print(next_wall, 'not cached')
#
#                 new_input = deepcopy(input)
#                 new_input[next_wall.row][next_wall.col] = '.'
#
#                 new_path_nodes, new_cost = a_star(new_input, start_pos, end_pos)
#                 new_len = new_cost[end_pos]
#                 savings[original_cost - new_len] += 1
#
# # pprint.pprint(savings)
# print('a', sum([num for saving, num in savings.items() if saving >= 100]))
savings_path = defaultdict(list)

with PrintTiming('b'):
    max_cheat_time_allowed = 20
    new_path, cost = a_star(input, start_pos, end_pos)
    original_cost = cost[end_pos]

    new_path_nodes = list(new_path.keys())
    nodes_len = len(new_path_nodes)
    for i, node in enumerate(new_path_nodes):
        if i % 1000 == 0:
            print(f'{i}/{nodes_len}', 'node', node)
        near_nodes = [near_node for near_node in new_path_nodes[new_path_nodes.index(node)+100:] if manhattan_distance(near_node, node) < max_cheat_time_allowed + 1 and near_node not in get_neighbors(input, node) and cost[node] < cost[near_node]]

        for near_node in near_nodes:
            try:
                cheat_path_nodes, cheat_cost = a_star(input, node, near_node, neighbors_func=get_cheat_neighbors)
            except IndexError:
                pass
            else:
                if cost[node] + cheat_cost[near_node] < cost[near_node] and cheat_cost[near_node] < max_cheat_time_allowed:
                    savings[cost[near_node] - cost[node] - cheat_cost[near_node]] += 1
                    savings_path[cost[near_node] - cost[node] - cheat_cost[near_node]].append(cheat_path_nodes)

        print(f'{sum([num for saving, num in savings.items() if saving >= 100]):,}')

pprint.pprint(savings)
#
# savings_path_to_print = savings_path[76][2]
# for row_i, row in enumerate(input):
#     for col_i, col in enumerate(row):
#         char_to_print = 'S' if Pos(row_i, col_i) == start_pos else 'M' if savings_path_to_print and Pos(row_i, col_i) in savings_path_to_print else col
#         print(char_to_print, end='')
#     print()

print('b', sum([num for saving, num in savings.items() if saving >= 100]))
