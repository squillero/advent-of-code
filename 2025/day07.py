# Advent of Code 2025 | https://adventofcode.com/2025/day/7
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from copy import deepcopy
from icecream import ic


INPUT_FILE_NAME = 'day07-test.txt'
# INPUT_FILE_NAME = 'day07-input.txt'

EMPTY = '.'
BEAM = '|'
SPLITTER = '^'
START = 'S'


def count_splits(diagram):
    """Count number of splits."""

    diagram_width = len(diagram[0])
    splits = 0
    for line in range(1, len(diagram)):
        previous_line = diagram[line - 1]
        current_line = diagram[line]
        for i in range(len(current_line)):
            if current_line[i] == EMPTY and previous_line[i] == START:
                current_line[i] = BEAM
            elif current_line[i] == EMPTY and previous_line[i] == BEAM:
                current_line[i] = BEAM
            elif current_line[i] == SPLITTER and previous_line[i] == BEAM:
                splits += 1
                if i > 0:
                    current_line[i - 1] = BEAM
                if i < diagram_width - 1:
                    current_line[i + 1] = BEAM
    # for line in diagram:
    #    print(''.join(line))
    return splits


def count_timelines(diagram):
    """Count number of alternative timelines."""

    diagram_width = len(diagram[0])

    # Convert diagram to number
    MAP = {EMPTY: 0, SPLITTER: -1, START: 1}
    diagram = [[MAP[s] for s in line] for line in diagram]

    for line in range(1, len(diagram)):
        previous_line = diagram[line - 1]
        current_line = diagram[line]
        for i in range(len(current_line)):
            if current_line[i] >= 0 and previous_line[i] >= 0:
                current_line[i] += previous_line[i]
            elif current_line[i] < 0 and previous_line[i] >= 0:
                if i > 0:
                    current_line[i - 1] += previous_line[i]
                if i < diagram_width - 1:
                    current_line[i + 1] += previous_line[i]

    return sum(n for n in diagram[-1] if n > 0)


def main():
    with open(INPUT_FILE_NAME) as file:
        diagram = [list(line[:-1]) for line in file]

    ic(count_splits(deepcopy(diagram)))
    ic(count_timelines(deepcopy(diagram)))


if __name__ == '__main__':
    main()
