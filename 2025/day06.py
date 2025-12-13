# Advent of Code 2025 | https://adventofcode.com/2025/day/5
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from functools import reduce
import operator
import numpy as np
from icecream import ic

INPUT_FILE_NAME = 'day06-test.txt'
INPUT_FILE_NAME = 'day06-input.txt'


# Yet another NumPy excercise, reasonably clean.
def cephalopod_math(filename):
    r"""Solve cephalopod math worksheet"""

    # Read worksheet
    with open(filename) as file:
        raw = [line.split() for line in file]
    nums = np.array(raw[:-1], dtype=int)
    ops = raw[-1]

    # Do math
    result = 0
    for col, op in enumerate(ops):
        if op == '*':
            result += reduce(operator.mul, nums[:, col], initial=1)
        elif op == '+':
            result += reduce(operator.add, nums[:, col], initial=0)
    return result


# A lot of parsing... reading by columns yields different numbers of operands
def cephalopod_math_inverted(filename):
    r"""Solve cephalopod math worksheet, cephalopod-style"""

    # Extract numbers column by column. Notez bien: This code sucks.
    with open(INPUT_FILE_NAME) as file:
        raw = np.array([list(line[:-1]) for line in file])
    tmp = raw[:, ::-1]
    ops = [o for o in tmp[-1] if o != ' ']
    tmp = tmp[:-1]
    row, cols = tmp.shape
    nums = list()
    line = list()
    for c in range(cols):
        t = ''.join(tmp[:, c]).strip()
        if t:
            line.append(int(t))
        else:
            nums.append(line)
            line = list()
    nums.append(line)

    # Do math
    result = 0
    for data, op in zip(nums, ops):
        if op == '*':
            result += reduce(operator.mul, data, 1)
        elif op == '+':
            result += reduce(operator.add, data, 0)

    return result


def main():
    result = cephalopod_math(INPUT_FILE_NAME)
    ic(result)
    result = cephalopod_math_inverted(INPUT_FILE_NAME)
    ic(result)


if __name__ == '__main__':
    main()
