# Advent of Code 2024 | https://adventofcode.com/2024/day/9
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from functools import cache
from collections import namedtuple
from icecream import ic

Rule = namedtuple('Rule', ['condition', 'transformation'])

# INPUT_FILE = 'day11-example.txt'
INPUT_FILE = 'day11-input.txt'


RULES = [
    Rule(condition=lambda s: s == 0, transformation=lambda s: [1]),
    Rule(
        condition=lambda s: len(str(s)) % 2 == 0,
        transformation=lambda s: [int(str(s)[: len(str(s)) // 2]), int(str(s)[len(str(s)) // 2 :])],
    ),
    Rule(condition=lambda s: True, transformation=lambda s: [s * 2024]),
]


@cache
def count_stones(stone, num):
    r"""Number of stones generatd by `stone` in `num` blinks (memoized)"""
    if num == 0:
        return 1
    transformation = next(t for c, t in RULES if c(stone))
    return sum(count_stones(s, num - 1) for s in transformation(stone))


def main():
    STONES = [int(s) for s in open(INPUT_FILE).read().split()]

    # --- Part One ---
    stones = STONES[:]
    num_blinks = 25
    for _ in range(num_blinks):
        new_stones = list()
        for s in stones:
            transformation = next(t for c, t in RULES if c(s))
            new_stones.extend(transformation(s))
        stones = new_stones
    num_stones = len(stones)
    ic(num_blinks, num_stones)

    # --- Part Two ---
    num_blinks = 75
    num_stones = sum(count_stones(s, num_blinks) for s in STONES)
    ic(num_blinks, num_stones)


if __name__ == '__main__':
    main()
