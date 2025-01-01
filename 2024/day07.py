# Advent of Code 2024 | https://adventofcode.com/2024/day/7
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from itertools import product
import operator
from tqdm.auto import tqdm
from icecream import ic


# INPUT_FILE = 'day07-example.txt'
INPUT_FILE = 'day07-input.txt'


def read_problem(filename):
    r"""Read the list of `<result> : <n1> ... <nk>`"""
    problem = list()
    for line in open(filename):
        value, tmp = line.split(':')
        problem.append((int(value), tuple(int(t) for t in tmp.split())))
    return problem


def evaluate_formula(numbers, operators):
    r"""Reversed stack-like evaluation"""
    numbers = list(reversed(numbers))
    for op in operators:
        numbers.append(op(numbers.pop(), numbers.pop()))
    return numbers[0]


def main():
    problem = read_problem(INPUT_FILE)

    # --- Part One ---
    operators = [operator.add, operator.mul]
    calibration = 0
    for value, numbers in tqdm(problem):
        if any(
            evaluate_formula(numbers, o) == value
            for o in product(operators, repeat=len(numbers) - 1)
        ):
            calibration += value
    ic(calibration)

    # --- Part Two ---
    operators.append(lambda a, b: int(str(a) + str(b)))
    calibration = 0
    for value, numbers in tqdm(problem):
        if any(
            evaluate_formula(numbers, o) == value
            for o in product(operators, repeat=len(numbers) - 1)
        ):
            calibration += value
    ic(calibration)


if __name__ == '__main__':
    main()
