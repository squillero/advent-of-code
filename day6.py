# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

import numpy as np
from icecream import ic


# INPUT_FILE = 'day6-example.txt'
INPUT_FILE = 'day6-input.txt'


DIRECTION_STEP = [
    (-1, 0),  # North: 0
    (0, 1),  # East: 1
    (1, 0),  # South: 2
    (0, -1),  # West: 3
]


def walk(pos, map_):
    r"""Proceeds straight until wall or end of map"""
    row, col, dir = pos
    while 0 <= row < map_.shape[0] and 0 <= col < map_.shape[1] and map_[row, col] != '#':
        map_[row, col] = 'o'
        last_pos = (row, col, dir)
        row += DIRECTION_STEP[dir][0]
        col += DIRECTION_STEP[dir][1]
    return last_pos if (0 <= row < map_.shape[0] and 0 <= col < map_.shape[1]) else None


def main():
    map_ = np.array([list(line.rstrip()) for line in open(INPUT_FILE)])
    # note: the cast is required as ndarrays are mutable...
    arrow = np.where(map_ == '^')
    pos = int(arrow[0]), int(arrow[1]), 3

    while pos is not None:
        pos = *pos[:2], (pos[2] + 1) % 4
        pos = walk(pos, map_)

    count = np.where(map_ == 'o')
    ic(len(count[0]))


if __name__ == '__main__':
    main()
