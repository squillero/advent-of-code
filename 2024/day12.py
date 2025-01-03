# Advent of Code 2024 | https://adventofcode.com/2024/day/12
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from dataclasses import dataclass
from itertools import accumulate
import numpy as np
from icecream import ic

# INPUT_FILE = 'day12-example.txt'
# INPUT_FILE = 'day12-example_small.txt'
INPUT_FILE = 'day12-input.txt'


@dataclass(frozen=True)
class GardenPosition:
    r: int
    c: int

    def __add__(self, other):
        return GardenPosition(self.r + other.r, self.c + other.c)

    def __call__(self, map_):
        return map_[self.r, self.c]

    @property
    def above(self):
        return self + GardenPosition(-1, 0)

    @property
    def below(self):
        return self + GardenPosition(1, 0)

    @property
    def right(self):
        return self + GardenPosition(0, 1)

    @property
    def left(self):
        return self + GardenPosition(0, -1)

    @property
    def neighbors(self):
        return {self.above, self.right, self.below, self.left}


SPECIAL = '•'


def poslist_to_idxs(positions):
    r"""Transforms a list of `GardenPosition` into `NumPy` indexes"""
    return [p.r for p in positions], [p.c for p in positions]


def find_region(map_):
    r"""Finds a region in the map"""
    r, c = np.where(map_ != SPECIAL)
    return GardenPosition(r[0], c[0]) if r.size else None


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
                if p(map_) == start(map_) and p not in area and p not in queue
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
            sides += p(map_) != p.above(map_) and not (
                p.left(map_) == p(map_) and p.left(map_) != p.left.above(map_)
            )
            sides += p(map_) != p.below(map_) and not (
                p.left(map_) == p(map_) and p.left(map_) != p.left.below(map_)
            )
            sides += p(map_) != p.right(map_) and not (
                p.above(map_) == p(map_) and p.above(map_) != p.above.right(map_)
            )
            sides += p(map_) != p.left(map_) and not (
                p.above(map_) == p(map_) and p.above(map_) != p.above.left(map_)
            )
        discountedPrice += sides * len(area)

        map_[poslist_to_idxs(area)] = SPECIAL

    ic(price)
    ic(discountedPrice)


if __name__ == '__main__':
    main()
