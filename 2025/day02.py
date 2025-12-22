# Advent of Code 2025 | https://adventofcode.com/2025/day/2
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from itertools import product
import re
from icecream import ic

INPUT_FILE_NAME = 'day02-test.txt'
# INPUT_FILE_NAME = 'day02-input.txt'


# Helper functions
def make_id(num_symbols: int) -> set[str]:
    """Generate a set of valid ids of length `num_symbols`"""
    return set(''.join(i) for i in product('0123456789', repeat=num_symbols) if i[0] != '0')


def invalid_ids_p1(num_digits: int) -> set[str]:
    """Generate the set of all **invalid** ids of length `num_digits` (part 1)"""
    return set(id_ * 2 for id_ in make_id(num_digits // 2)) if num_digits % 2 == 0 else set()


def invalid_ids_p2(num_digits: int) -> set[str]:
    """Generate the set of all **invalid** ids of length `num_digits` (part 2)"""
    invalid = set()
    for n in range(1, num_digits):
        if num_digits % n == 0:
            invalid |= {i * (num_digits // n) for i in make_id(n)}
    return invalid


# First idea: create all illegal ids and check if they are inside the ranges.
# Probably faster if the ranges are huge.
def solve_by_generating(id_ranges: list[tuple[str, str]]) -> None:
    """Display the sum of all invalid ids in a list of ranges"""

    # Part 1
    tot_invalid = 0
    for from_, to_ in id_ranges:
        for id_ in set.union(*[invalid_ids_p1(d) for d in range(len(from_), len(to_) + 1)]):
            if int(from_) <= int(id_) <= int(to_):
                tot_invalid += int(id_)
    ic(tot_invalid)

    # Part 2
    tot_invalid = 0
    for from_, to_ in id_ranges:
        for id_ in set.union(*[invalid_ids_p2(d) for d in range(len(from_), len(to_) + 1)]):
            if int(from_) <= int(id_) <= int(to_):
                tot_invalid += int(id_)
    ic(tot_invalid)


# Second idea: generate all ids in the ranges and check if they are valid
# using a regex. Probably slower, but regexs are trivial.
def solve_by_checking(id_ranges: list[tuple[str, str]]) -> None:
    """Display the sum of all invalid ids in a list of ranges"""

    # Part 1
    invalid = re.compile(r'^(.+)\1$')
    tot_invalid = 0
    for from_, to_ in id_ranges:
        for n in range(int(from_), int(to_) + 1):
            if invalid.match(str(n)):
                tot_invalid += n
    ic(tot_invalid)

    # Part 2
    invalid = re.compile(r'^(.+)\1+$')
    tot_invalid = 0
    for from_, to_ in id_ranges:
        for n in range(int(from_), int(to_) + 1):
            if invalid.match(str(n)):
                tot_invalid += n
    ic(tot_invalid)


def main():
    ranges = list()
    with open(INPUT_FILE_NAME) as file:
        for r in file.read().split(','):
            ranges.append(tuple(r.split('-')))

    solve_by_generating(ranges)  # maybe faster ;-)
    solve_by_checking(ranges)  # kinda slower :-(


if __name__ == '__main__':
    main()
