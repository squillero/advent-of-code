# Advent of Code 2024 | https://adventofcode.com/2024/day/7
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from itertools import product
import operator
from tqdm.auto import tqdm
from icecream import ic


# INPUT_FILE = 'day7-example.txt'
INPUT_FILE = 'day7-input.txt'

OPERATORS = [operator.add, operator.mul]


def read_problem(filename):
    problem = list()
    for line in open(filename):
        value, tmp = line.split(':')
        problem.append((int(value), tuple(int(t) for t in tmp.split())))
    return problem


def evaluate_equation(nums, ops):
    nums = list(reversed(nums))
    for op in ops:
        nums.append(op(nums.pop(), nums.pop()))
    return nums[0]


def main():
    problem = read_problem(INPUT_FILE)

    calibration = 0
    for value, numbers in tqdm(problem):
        if any(
            evaluate_equation(numbers, o) == value
            for o in product(OPERATORS, repeat=len(numbers) - 1)
        ):
            calibration += value
    ic(calibration)

    OPERATORS.append(lambda a, b: int(str(a) + str(b)))
    calibration = 0
    for value, numbers in tqdm(problem):
        if any(
            evaluate_equation(numbers, o) == value
            for o in product(OPERATORS, repeat=len(numbers) - 1)
        ):
            calibration += value
    ic(calibration)


if __name__ == '__main__':
    main()
