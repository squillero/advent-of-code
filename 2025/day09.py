# Advent of Code 2025 | https://adventofcode.com/2025/day/9
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import namedtuple
from itertools import combinations

import numpy as np
from icecream import ic

# INPUT_FILE_NAME = 'day09-test.txt'
INPUT_FILE_NAME = 'day09-input.txt'

Tile = namedtuple('Tile', ['x', 'y'])


def area(t1: Tile, t2: Tile) -> int:
    r"""Calculate the are of the square t1-t2, whatever order t1, t2"""
    return (abs(t1.x - t2.x) + 1) * (abs(t1.y - t2.y) + 1)


def check_green(green_range, t1, t2):
    r"""Check if the square t1-t2 fits into the green area"""
    xs, ys = min(t1.x, t2.x), min(t1.y, t2.y)
    xe, ye = max(t1.x, t2.x), max(t1.y, t2.y)
    return np.all(green_range[ys : ye + 1, 0] <= xs) and np.all(green_range[ys : ye + 1, 1] >= xe)


def main():
    with open(INPUT_FILE_NAME) as file:
        red_tiles = [Tile(*map(int, line.split(','))) for line in file]

    # Part 1 -- simplistic one liner
    t1, t2 = max(combinations(red_tiles, r=2), key=lambda t: area(*t))
    ic(t1, t2, area(t1, t2))

    # Part 2
    # For each column (y) calculate the extension of the green area (x_min, x_max)
    # then use the same, old, simplistic one liner on valid corners
    green_range = np.empty((1 + max(t.y for t in red_tiles), 2), dtype=int)
    green_range[:, 0] = 1 + max(t.x for t in red_tiles)
    green_range[:, 1] = -1
    for t1, t2 in zip(red_tiles, red_tiles[1:] + [red_tiles[0]]):
        if t1.x == t2.x:
            # Vertical line (swipe on y)
            x, ys, ye = t1.x, min(t1.y, t2.y), max(t1.y, t2.y)
            green_range[ys : ye + 1, 0] = np.minimum(green_range[ys : ye + 1, 0], x)
            green_range[ys : ye + 1, 1] = np.maximum(green_range[ys : ye + 1, 1], x)
        elif t1.y == t2.y:
            # Horizontal line (swipe on x)
            y, xs, xe = t1.y, min(t1.x, t2.x), max(t1.x, t2.x)
            green_range[y, 0] = min(green_range[y, 0], xs)
            green_range[y, 1] = max(green_range[y, 1], xe)
        else:
            assert "Dho!?"

    # Let's use an explicit generator for readability
    valid_corners = (
        (t1, t2) for t1, t2 in combinations(red_tiles, r=2) if check_green(green_range, t1, t2)
    )
    t1, t2 = max(valid_corners, key=lambda t: area(*t))
    ic(t1, t2, area(t1, t2))


if __name__ == '__main__':
    main()
