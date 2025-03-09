# Advent of Code 2024 | https://adventofcode.com/2024/day/15
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from itertools import product
import numpy as np
from icecream import ic

EMPTY = '.'
WALL = '#'
BOX = 'O'
ROBOT = '@'

# INPUT_FILE = 'day15-input.txt'
# INPUT_FILE = 'day15-example.txt'
INPUT_FILE = 'day15-example_small.txt'

MAP = None


def print_map():
    r"""Debug function"""
    print('\n'.join(''.join(MAP[r]) for r in range(MAP.shape[0])))


def robot_position():
    r"""Return a tuple with the robot poition"""
    return tuple(_[0] for _ in np.where(MAP == '@'))


def gps(point):
    r"""Return the Goods Positioning System"""
    return 100 * point[0] + point[1]


def next(point, direction):
    r"""Returns the `next` point in the given direction"""
    if direction == '^':
        return point[0] - 1, point[1]
    elif direction == '>':
        return point[0], point[1] + 1
    elif direction == 'v':
        return point[0] + 1, point[1]
    elif direction == '<':
        return point[0], point[1] - 1
    else:
        return None


def push(point, direction):
    r"""Push the object in `point` in the given `direction`"""

    next_point = next(point, direction)
    if MAP[next_point] == BOX:
        push(next_point, direction)
    if MAP[next_point] == EMPTY:
        MAP[next_point] = MAP[point]
        MAP[point] = EMPTY


def push2(point, direction):
    r"""Push the object in `point` in the given `direction`"""

    next_point = next(point, direction)
    if MAP[next_point] == '#':
        return
    if direction == '<' or direction == '>':
        if MAP[next_point] == '[' or MAP[next_point] == ']':
            push(next_point, direction)
    if MAP[next_point] == EMPTY:
        MAP[next_point] = MAP[point]
        MAP[point] = EMPTY


def main():
    global MAP
    map, path = open(INPUT_FILE).read().split('\n\n')
    path = path.replace('\n', '')
    initial_map = np.array([list(_) for _ in map.split()], dtype='U1')
    MAP = initial_map.copy()

    # --- Part One ---
    for step in path:
        push(robot_position(), step)
    total_gps = 0
    for p in product(*[range(_) for _ in MAP.shape]):
        if MAP[p] == BOX:
            total_gps += gps(p)
    ic(total_gps)

    # --- Part Two ---
    new_map = np.empty((MAP.shape[0], 2 * MAP.shape[1]), dtype='U1')
    for r, c in product(*[range(_) for _ in MAP.shape]):
        if initial_map[r, c] == '#':
            new_map[r, c * 2] = '#'
            new_map[r, c * 2 + 1] = '#'
        elif initial_map[r, c] == 'O':
            new_map[r, c * 2] = '['
            new_map[r, c * 2 + 1] = ']'
        elif initial_map[r, c] == '.':
            new_map[r, c * 2] = '.'
            new_map[r, c * 2 + 1] = '.'
        elif initial_map[r, c] == '@':
            new_map[r, c * 2] = '@'
            new_map[r, c * 2 + 1] = '.'
    print_map()
    MAP = new_map
    print_map()


if __name__ == '__main__':
    main()
