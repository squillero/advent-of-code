# Advent of Code 2024 | https://adventofcode.com/2024/day/1
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from icecream import ic

INPUT_FILE = 'day1-input.txt'


def read_lists(filename):
    r"""Read left/right lists from file"""
    right_list = list()
    left_list = list()
    with open(filename) as file:
        for line in file:
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))
    return left_list, right_list


def main():
    left_list, right_list = read_lists(INPUT_FILE)

    # --- Part One ---
    distance = sum(abs(l - r) for l, r in zip(sorted(left_list), sorted(right_list)))
    ic(distance)

    # --- Part Two ---
    similarity = sum(i * right_list.count(i) for i in left_list)
    ic(similarity)


if __name__ == '__main__':
    main()
