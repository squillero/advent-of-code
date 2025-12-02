# Advent of Code 2025 | https://adventofcode.com/2025/day/1
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from icecream import ic

INPUT_FILE_NAME = 'day01-test.txt'
INPUT_FILE_NAME = 'day01-input.txt'


def part_one(file_name):
    dial = 50
    password = 0
    with open(INPUT_FILE_NAME) as file:
        for line in file:
            d, offset = line[0], int(line[1:])
            dial += offset if d == 'R' else -offset
            if dial % 100 == 0:
                password += 1
    return password


def part_two(file_name):
    dial = 50
    password = 0
    with open(INPUT_FILE_NAME) as file:
        for line in file:
            step = +1 if line[0] == 'R' else -1
            for _ in range(abs(int(line[1:]))):
                dial += step
                if dial % 100 == 0:
                    password += 1
    return password


def main():
    password = part_one(INPUT_FILE_NAME)
    ic(password)
    password = part_two(INPUT_FILE_NAME)
    ic(password)


if __name__ == '__main__':
    main()
