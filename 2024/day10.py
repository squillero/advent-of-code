# Advent of Code 2024 | https://adventofcode.com/2024/day/9
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import namedtuple
import numpy as np
from icecream import ic


# INPUT_FILE = 'day10-example.txt'
INPUT_FILE = 'day10-input.txt'

Pos = namedtuple('Pos', ['r', 'c'])


def follow_trails(map_, current_trails):
    r"""Advance all possible single steps in the given `current_trails`"""
    valid_trails = list()
    for trail in current_trails:
        pos = trail[-1]
        for p in [
            Pos(pos.r, pos.c - 1),
            Pos(pos.r + 1, pos.c),
            Pos(pos.r, pos.c + 1),
            Pos(pos.r - 1, pos.c),
        ]:
            if map_[p] == map_[pos] + 1:
                valid_trails.append(trail[:] + [p])
    if valid_trails:
        return follow_trails(map_, valid_trails)
    else:
        return current_trails


def main():
    map_ = np.array([[int(c) for c in line.rstrip()] for line in open(INPUT_FILE)])
    map_ = np.pad(map_, pad_width=1, constant_values=-1)

    # --- Part One ---
    trails = follow_trails(map_, [[Pos(r, c)] for r, c in zip(*np.where(map_ == 0))])
    trailhead_score = len(set((t[0], t[-1]) for t in trails))
    ic(trailhead_score)

    # --- Part Two ---
    num_trails = len(trails)
    ic(num_trails)


if __name__ == '__main__':
    main()
