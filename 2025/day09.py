# Advent of Code 2025 | https://adventofcode.com/2025/day/9
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import namedtuple
from itertools import combinations
from icecream import ic

INPUT_FILE_NAME = 'day09-test.txt'
INPUT_FILE_NAME = 'day09-input.txt'

Tile = namedtuple('Tile', ['c', 'r'])


def area(t1: Tile, t2: Tile) -> int:
    return abs(t1.r - t2.r + 1) * abs(t1.c - t2.c + 1)


def main():
    with open(INPUT_FILE_NAME) as file:
        tiles = [Tile(*map(int, line.split(','))) for line in file]

    # Part 1
    t1, t2 = max(combinations(tiles, r=2), key=lambda t: area(*t))
    ic(t1, t2, area(t1, t2))


if __name__ == '__main__':
    main()
