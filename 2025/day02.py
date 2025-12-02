# Advent of Code 2025 | https://adventofcode.com/2025/day/2
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from itertools import product
import re
from icecream import ic

# INPUT_FILE_NAME = 'day02-test.txt'
INPUT_FILE_NAME = 'day02-input.txt'


def create_id(symbols, length) -> set[str]:
    return set(''.join(d) for d in product(symbols, repeat=length))


def invalid_ids_p1(num_symbols) -> set[str]:
    if num_symbols == 0:
        return set()
    else:
        return set(
            p1 + p2
            for p1, p2 in product(
                create_id('123456789', 1), create_id('0123456789', num_symbols - 1)
            )
        )


def invalid_ids_p2(num_digits):
    invalid = set()
    for n in range(1, num_digits):
        if num_digits % n == 0:
            invalid |= {i * (num_digits // n) for i in invalid_ids_p1(n)}
    return invalid


# First idea: create all illegal ids and check if they are in range
def generate_all_illegal_ids(id_ranges):
    # Part 1
    tot_invalid = 0
    for from_, to_ in id_ranges:
        for id_ in set.union(
            *[invalid_ids_p1(d) for d in range(len(from_) // 2, len(to_) // 2 + 1)]
        ):
            id_ *= 2
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


# Second idea: create a check for illegal ones using regex
def generate_all_ids(id_ranges):
    pattern = re.compile(r'^(.+)\1$')
    tot_invalid = 0
    for from_, to_ in id_ranges:
        for n in range(int(from_), int(to_) + 1):
            if pattern.match(str(n)):
                tot_invalid += n
    ic(tot_invalid)

    pattern = re.compile(r'^(.+)\1+$')
    tot_invalid = 0
    for from_, to_ in id_ranges:
        for n in range(int(from_), int(to_) + 1):
            if pattern.match(str(n)):
                tot_invalid += n
    ic(tot_invalid)


def main():
    ranges = list()
    with open(INPUT_FILE_NAME) as file:
        for r in file.read().split(','):
            ranges.append(tuple(r.split('-')))

    # v1 - faster ;-)
    generate_all_illegal_ids(ranges)

    # v2 - slower :-(
    generate_all_ids(ranges)


if __name__ == '__main__':
    main()
