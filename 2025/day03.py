# Advent of Code 2025 | https://adventofcode.com/2025/day/3
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from itertools import combinations
from icecream import ic

INPUT_FILE_NAME = 'day03-test.txt'
# INPUT_FILE_NAME = 'day03-input.txt'


def main():
    with open(INPUT_FILE_NAME) as file:
        batteries = file.read().split()

    # = [Part 1] ============================================================
    NUM_BATTERIES = 2
    # Easy one-liner...
    total_joltage = 0
    for battery in batteries:
        total_joltage += max(int(a + b) for a, b in combinations(battery, NUM_BATTERIES))
    ic(total_joltage)

    # = [Part 2] ============================================================
    NUM_BATTERIES = 12
    # Yeuch, that would be 1,050,421,051,106,700 combinations for each bank...
    # Let select the batteries with the biggest joltage one by one.
    total_joltage = 0
    for battery in batteries:
        selected = ''
        for pos in range(NUM_BATTERIES):
            # Leave out enough batteries to complete the task later
            b = max(battery[: len(battery) - NUM_BATTERIES + 1 + pos])
            # Discard all bateries on the left of the selected one
            battery = battery[battery.index(b) + 1 :]
            selected += b
        total_joltage += int(selected)
    ic(total_joltage)


if __name__ == '__main__':
    main()
