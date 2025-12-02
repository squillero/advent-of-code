# Advent of Code 2025 | https://adventofcode.com/2025/day/2
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from itertools import product
from icecream import ic

# INPUT_FILE_NAME = 'day02-test.txt'
INPUT_FILE_NAME = 'day02-input.txt'


def invalid_ids(num_digits):
    if num_digits % 2 == 1:
        return
    for x in product('0123456789', repeat=num_digits // 2):
        if x[0] == '0':
            continue  # Yeuch
        yield ''.join(x) * 2


def invalid_ids_v2(num_digits):
    invalid = set()
    for c0 in '123456789':
        for cn in (
            ''.join(c) for s in range(num_digits // 2) for c in product('0123456789', repeat=s)
        ):
            id_ = (c0 + cn) * (num_digits // len(c0 + cn))
            if len(id_) == num_digits:
                invalid.add(id_)
    return invalid


def main():
    with open(INPUT_FILE_NAME) as file:
        id_ranges = file.read().split(',')

    # v1
    tot_invalid = 0
    for id_range in id_ranges:
        from_, to_ = id_range.split('-')
        for digits in range(len(from_), len(to_) + 1):
            for id_ in invalid_ids(digits):
                if int(from_) <= int(id_) <= int(to_):
                    tot_invalid += int(id_)
                    # ic(id_)
    ic(tot_invalid)

    # v2
    tot_invalid = 0
    for id_range in id_ranges:
        from_, to_ = id_range.split('-')
        for digits in range(len(from_), len(to_) + 1):
            for id_ in invalid_ids_v2(digits):
                if int(from_) <= int(id_) <= int(to_):
                    tot_invalid += int(id_)
                    # ic(id_)
    ic(tot_invalid)


if __name__ == '__main__':
    main()
