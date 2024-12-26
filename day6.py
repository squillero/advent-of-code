# Advent of Code 2024 | https://adventofcode.com/2024/day/6
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD


from collections import namedtuple
import numpy as np
from tqdm.auto import tqdm
from icecream import ic


INPUT_FILE = 'day6-example.txt'
INPUT_FILE = 'day6-input.txt'


# Directions: North ⟳ East ⟳ South ⟳ West
DIRECTION_STEP = [(-1, 0), (0, 1), (1, 0), (0, -1)]
CURRENT_POSITION = '^'
OBSTACLE = '#'
STEPPED_TILE = 'X'
NEW_OBSTRUCTION = 'O'

Position = namedtuple('Position', ['row', 'col', 'dir'])


def walk_straight(pos, map_):
    r"""Proceeds straight until wall or end of map"""
    while (
        0 <= pos.row < map_.shape[0]
        and 0 <= pos.col < map_.shape[1]
        and map_[pos.row, pos.col] != OBSTACLE
    ):
        map_[pos.row, pos.col] = STEPPED_TILE
        last_pos = pos
        pos = Position(
            pos.row + DIRECTION_STEP[pos.dir][0], pos.col + DIRECTION_STEP[pos.dir][1], pos.dir
        )
    return last_pos if (0 <= pos.row < map_.shape[0] and 0 <= pos.col < map_.shape[1]) else None


def stuck_in_loop(pos, map_):
    r"""Check if guard is stuck in a circular path"""

    stepped = set()
    while 0 <= pos.row < map_.shape[0] and 0 <= pos.col < map_.shape[1]:
        stepped.add(pos)
        if map_[pos.row, pos.col] == OBSTACLE or map_[pos.row, pos.col] == NEW_OBSTRUCTION:
            pos = Position(
                pos.row - DIRECTION_STEP[pos.dir][0],
                pos.col - DIRECTION_STEP[pos.dir][1],
                (pos.dir + 1) % 4,
            )
        pos = Position(
            pos.row + DIRECTION_STEP[pos.dir][0], pos.col + DIRECTION_STEP[pos.dir][1], pos.dir
        )
        if pos in stepped:
            return True
    return False


def main():
    map_ = np.array([list(line.rstrip()) for line in open(INPUT_FILE)])
    rows, cols = np.where(map_ == CURRENT_POSITION)
    # note: the cast is required (ndarrays are mutable)
    initial_pos = Position(int(rows[0]), int(cols[0]), 0)

    # --- Part One ---
    pos = Position(initial_pos.row, initial_pos.col, -1)
    while pos is not None:
        pos = walk_straight(Position(pos.row, pos.col, (pos.dir + 1) % 4), map_)
    stepped_positions = int(np.sum(map_ == STEPPED_TILE))
    ic(stepped_positions)

    # --- Part Two ---
    selectable_positions = 0
    map_[initial_pos.row, initial_pos.col] = CURRENT_POSITION
    for r, c in tqdm(zip(*np.where(map_ == STEPPED_TILE)), total=stepped_positions - 1):
        map_[r, c] = NEW_OBSTRUCTION
        selectable_positions += stuck_in_loop(initial_pos, map_)
        map_[r, c] = STEPPED_TILE
    ic(selectable_positions)


if __name__ == '__main__':
    main()
