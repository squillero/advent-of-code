# Advent of Code 2025 | https://adventofcode.com/2025/day/1
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from icecream import ic

INPUT_FILE_NAME = 'day01-test.txt'
# INPUT_FILE_NAME = 'day01-input.txt'

TOTAL_TICKS = 100


# Just roll...
# Notez bien: No need to reset the dial (-1 % 100 == 99)
def part_one(file_name: str) -> int:
    """Turn dial and check position at the end"""

    dial = 50
    password = 0
    with open(file_name) as file:
        for line in file:
            dial += int(line[1:]) if line[0] == 'R' else -int(line[1:])
            if dial % TOTAL_TICKS == 0:
                password += 1
    return password


# Just roll, one click at a time.
def part_two(file_name: str) -> int:
    """Turn dial and check position after each tick"""

    dial = 50
    password = 0
    with open(file_name) as file:
        for line in file:
            step = +1 if line[0] == 'R' else -1
            for _ in range(abs(int(line[1:]))):
                dial += step
                if dial % TOTAL_TICKS == 0:
                    password += 1
    return password


def main():
    password = part_one(INPUT_FILE_NAME)
    ic(password)
    password = part_two(INPUT_FILE_NAME)
    ic(password)


if __name__ == '__main__':
    main()
