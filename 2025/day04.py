# Advent of Code 2025 | https://adventofcode.com/2025/day/4
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from itertools import product
import numpy as np
from icecream import ic

# INPUT_FILE_NAME = 'day04-test.txt'
INPUT_FILE_NAME = 'day04-input.txt'


# An easy NumPy excercise.
def count_accessible_rolls_part1(grid: np.ndarray) -> int:
    r"""Count rolls of paper can be accessed by a forklift"""

    dimx, dimy = grid.shape
    adjacent_rolls = np.astype(grid == '@', int)
    padded_grid = np.pad(adjacent_rolls, 1)
    adjacent_rolls *= -1
    for ox, oy in product([-1, 0, 1], repeat=2):
        adjacent_rolls += padded_grid[ox + 1 : ox + dimx + 1, oy + 1 : oy + dimy + 1]
    accessible_rolls = np.logical_and(grid == '@', adjacent_rolls < 4)
    return accessible_rolls.sum()


# I love NumPy boolean masks!
def count_accessible_rolls_part2(grid: np.ndarray) -> int:
    r"""Count rolls of paper can be accessed by a forklift (part2)"""

    dimx, dimy = grid.shape

    total_removed = 0
    last_removed = True
    while last_removed:
        adjacent_rolls = np.astype(grid == '@', int)
        padded_grid = np.pad(adjacent_rolls, 1)
        adjacent_rolls *= -1
        for ox, oy in product([-1, 0, 1], repeat=2):
            adjacent_rolls += padded_grid[ox + 1 : ox + dimx + 1, oy + 1 : oy + dimy + 1]
        accessible_rolls = np.logical_and(grid == '@', adjacent_rolls < 4)
        last_removed = accessible_rolls.sum()
        total_removed += last_removed
        grid[accessible_rolls] = '.'  # remove rolls
    return total_removed


def main():
    with open(INPUT_FILE_NAME) as file:
        grid = np.array([list(l.strip()) for l in file])

    ic(count_accessible_rolls_part1(grid))
    ic(count_accessible_rolls_part2(grid))


if __name__ == '__main__':
    main()
