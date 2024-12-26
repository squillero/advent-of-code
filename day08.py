# Advent of Code 2024 | https://adventofcode.com/2024/day/8
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import namedtuple, defaultdict
from itertools import product, permutations
import numpy as np
from icecream import ic


# INPUT_FILE = 'day8-example.txt'
INPUT_FILE = 'day8-input.txt'

Position = namedtuple('Position', ['row', 'col'])
EMPTY_SQUARE = '.'
ANTINODE_SQUARE = '#'


def antinode(s1, s2):
    return Position(2 * s2.row - s1.row, 2 * s2.col - s1.col)


def inside_map(pos, map_):
    return 0 <= pos.row < map_.shape[0] and 0 <= pos.col < map_.shape[1]


def parse_map(map_):
    stations = defaultdict(set)
    for r, c in product(range(map_.shape[0]), range(map_.shape[1])):
        if map_[r, c] != EMPTY_SQUARE:
            stations[str(map_[r, c])].add(Position(r, c))

    return stations


def main():
    map_ = np.array([list(line.rstrip()) for line in open(INPUT_FILE)])
    stations = parse_map(map_)

    # --- Part One ---
    for _, stats in stations.items():
        for s1, s2 in permutations(stats, 2):
            anti = antinode(s1, s2)
            if inside_map(anti, map_):
                map_[anti] = ANTINODE_SQUARE
    unique_antinodes = int(np.sum(map_ == ANTINODE_SQUARE))
    ic(unique_antinodes)

    # --- Part Two ---
    for _, stats in stations.items():
        assert len(stats) > 1
        for s in stats:
            map_[s] = ANTINODE_SQUARE
        for s1, s2 in permutations(stats, 2):
            anti = antinode(s1, s2)
            while inside_map(anti, map_):
                map_[anti] = ANTINODE_SQUARE
                s1, s2 = s2, anti
                anti = antinode(s1, s2)
    unique_antinodes = int(np.sum(map_ == ANTINODE_SQUARE))
    ic(unique_antinodes)


if __name__ == '__main__':
    main()
