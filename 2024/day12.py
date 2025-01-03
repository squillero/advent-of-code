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
class Position:
    r: int
    c: int

    def __add__(self, other):
        return Position(self.r + other.r, self.c + other.c)

    def __call__(self, garden):
        return garden[self.r, self.c]

    @property
    def above(self):
        return self + Position(-1, 0)

    @property
    def below(self):
        return self + Position(1, 0)

    @property
    def right(self):
        return self + Position(0, 1)

    @property
    def left(self):
        return self + Position(0, -1)

    @property
    def neighbors(self):
        return {self.above, self.right, self.below, self.left}


SPECIAL = '•'


def poslist_to_idxs(positions):
    r"""Transforms a list of `Position` into `NumPy` indexes"""
    return [p.r for p in positions], [p.c for p in positions]


def find_region(garden):
    r"""Finds a region in the map"""
    r, c = np.where(garden != SPECIAL)
    return Position(r[0], c[0]) if r.size else None


def flood(garden, start):
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
                if p(garden) == start(garden) and p not in area and p not in queue
            ]
        )
    return area


def main():
    garden = np.array([list(line.rstrip()) for line in open(INPUT_FILE)])
    garden = np.pad(garden, pad_width=1, constant_values=SPECIAL)

    # --- Part One and Part Two ---
    price = 0
    discountedPrice = 0
    while pos := find_region(garden):
        area = flood(garden, pos)
        *_, borders = accumulate(area, lambda x, p: x + list(p.neighbors - area), initial=list())
        price += len(area) * len(borders)

        sides = 0
        for p in area:
            sides += p(garden) != p.above(garden) and not (
                p.left(garden) == p(garden) and p.left(garden) != p.left.above(garden)
            )
            sides += p(garden) != p.below(garden) and not (
                p.left(garden) == p(garden) and p.left(garden) != p.left.below(garden)
            )
            sides += p(garden) != p.right(garden) and not (
                p.above(garden) == p(garden) and p.above(garden) != p.above.right(garden)
            )
            sides += p(garden) != p.left(garden) and not (
                p.above(garden) == p(garden) and p.above(garden) != p.above.left(garden)
            )
        discountedPrice += sides * len(area)

        garden[poslist_to_idxs(area)] = SPECIAL

    ic(price)
    ic(discountedPrice)


if __name__ == '__main__':
    main()
