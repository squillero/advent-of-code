# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from icecream import ic

INPUT_FILE = 'day1-input.txt'


def read_lists(filename):
    r"""Read left/right lists from file"""
    right_list = list()
    left_list = list()
    try:
        with open(filename) as file:
            for line in file:
                left, right = line.split()
                left_list.append(int(left))
                right_list.append(int(right))
    except OSError as problem:
        exit(problem)
    return left_list, right_list


def main():
    r"""Standard entry point"""
    left_list, right_list = read_lists(INPUT_FILE)

    distance = sum(abs(l - r) for l, r in zip(sorted(left_list), sorted(right_list)))
    ic(distance)

    similarity = sum(i * right_list.count(i) for i in left_list)
    ic(similarity)


if __name__ == '__main__':
    main()
