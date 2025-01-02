# Advent of Code 2024 | https://adventofcode.com/2024/day/12
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import namedtuple
from dataclasses import dataclass
from itertools import accumulate, product
import numpy as np
from icecream import ic

# INPUT_FILE = 'day12-example.txt'
# INPUT_FILE = 'day12-example_small.txt'
INPUT_FILE = 'day12-input.txt'


@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def __add__(self, other):
        return Pos(self.r + other.r, self.c + other.c)

    @property
    def above(self):
        return self + Pos(-1, 0)

    @property
    def below(self):
        return self + Pos(1, 0)

    @property
    def right(self):
        return self + Pos(0, 1)

    @property
    def left(self):
        return self + Pos(0, -1)

    @property
    def neighbors(self):
        return {self.above, self.right, self.below, self.left}

    @property
    def i(self):
        return self.r, self.c


SPECIAL = '•'


def poslist_to_idxs(positions):
    r"""Transforms a list of `Pos` into `NumPy` indexes"""
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
                for p in pos.neighbors
                if map_[p.i] == map_[start.i] and p not in area and p not in queue
            ]
        )
    return area


def main():
    map_ = np.array([list(line.rstrip()) for line in open(INPUT_FILE)])
    map_ = np.pad(map_, pad_width=1, constant_values=SPECIAL)

    # --- Part One and Part Two ---
    price = 0
    discountedPrice = 0
    while pos := find_region(map_):
        area = flood(map_, pos)
        *_, borders = accumulate(area, lambda x, p: x + list(p.neighbors - area), initial=list())
        price += len(area) * len(borders)

        sides = 0
        for p in area:
            sides += map_[p.i] != map_[p.above.i] and not (
                map_[p.left.i] == map_[p.i] and map_[p.left.i] != map_[p.left.above.i]
            )
            sides += map_[p.i] != map_[p.below.i] and not (
                map_[p.left.i] == map_[p.i] and map_[p.left.i] != map_[p.left.below.i]
            )
            sides += map_[p.i] != map_[p.right.i] and not (
                map_[p.above.i] == map_[p.i] and map_[p.above.i] != map_[p.above.right.i]
            )
            sides += map_[p.i] != map_[p.left.i] and not (
                map_[p.above.i] == map_[p.i] and map_[p.above.i] != map_[p.above.left.i]
            )
        discountedPrice += sides * len(area)

        map_[poslist_to_idxs(area)] = SPECIAL

    ic(price)
    ic(discountedPrice)


if __name__ == '__main__':
    main()
