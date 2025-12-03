# Advent of Code 2025 | https://adventofcode.com/2025/day/3
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from itertools import combinations
from icecream import ic

# INPUT_FILE_NAME = 'day03-test.txt'
INPUT_FILE_NAME = 'day03-input.txt'


def main():
    with open(INPUT_FILE_NAME) as file:
        batteries = file.read().split()

    # easy problem, one-liner
    total_joltage = 0
    for battery in batteries:
        total_joltage += max(int(a + b) for a, b in combinations(battery, 2))
    ic(total_joltage)

    # 12 batteries are too much for using `combinations`
    # idea: pick the biggest battery, but leaving enough batteries after it
    NUM_BATTERIES = 12
    total_joltage = 0
    for battery in batteries:
        selected = ''
        for pos in range(NUM_BATTERIES):
            b = max(battery[: len(battery) - NUM_BATTERIES + 1 + pos])
            battery = battery[battery.index(b) + 1 :]
            selected += b
        total_joltage += int(selected)
    ic(total_joltage)


if __name__ == '__main__':
    main()
