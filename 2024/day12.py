# Advent of Code 2024 | https://adventofcode.com/2024/day/12
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import namedtuple
from itertools import accumulate
import numpy as np
from icecream import ic

# INPUT_FILE = 'day12-example.txt'
INPUT_FILE = 'day12-input.txt'

SPECIAL = '•'
Pos = namedtuple('Pos', ['r', 'c'])


def get_neighbors(pos):
    r"""Generates the set of neighbors (N, E, S, W)"""
    return {Pos(pos.r + r, pos.c + c) for r, c in [(0, -1), (1, 0), (0, +1), (-1, 0)]}


def poslist_to_idxs(positions):
    r"""Transforms a list of `Pos` into `NumPy` index:es"""
    return [p.r for p in positions], [p.c for p in positions]


def find_region(map_):
    r"""Finds a region in the map"""
    r, c = np.where(map_ != SPECIAL)
    return Pos(r[0], c[0]) if r.size else None


def flood(map_, start):
    r"""Flood fills region starting from `start`, returns area and perimeter"""
    area = set()
    queue = [start]
    while queue:
        pos = queue.pop()
        area.add(pos)
        queue.extend(
            [
                p
                for p in get_neighbors(pos)
                if map_[p] == map_[start] and p not in area and p not in queue
            ]
        )

    *_, neighbors = accumulate(area, lambda x, p: x + list(get_neighbors(p) - area), initial=list())
    map_[poslist_to_idxs(area)] = SPECIAL

    return len(area), len(neighbors)


def main():
    map_ = np.array([list(line.rstrip()) for line in open(INPUT_FILE)])
    map_ = np.pad(map_, pad_width=1, constant_values=SPECIAL)

    # --- Part One ---
    price = 0
    while pos := find_region(map_):
        a, p = flood(map_, pos)
        price += a * p
    ic(price)

    # --- Part Two ---


if __name__ == '__main__':
    main()
