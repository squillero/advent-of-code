# Advent of Code 2024 | https://adventofcode.com/2024/day/3
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD


import re
from icecream import ic

# INPUT_FILE = 'day03-example.txt'
INPUT_FILE = 'day03-input.txt'


def main():
    text = open(INPUT_FILE).read()
    ops = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

    # --- Part One ---
    result = 0
    for x, y in re.findall(ops, text):
        result += int(x) * int(y)
    ic(result)

    # --- Part Two ---
    result = 0
    enabled = re.findall(
        r'''(?:(?<=do\(\))|^)(.*?)(?:(?=don't\(\))|$)''', text, flags=re.DOTALL
    )
    for x, y in re.findall(ops, ' '.join(enabled)):
        result += int(x) * int(y)
    ic(result)


if __name__ == '__main__':
    main()
