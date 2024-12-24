# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

import re
from icecream import ic

# INPUT_FILE = 'day3-example.txt'
INPUT_FILE = 'day3-input.txt'


def main():
    text = open(INPUT_FILE).read()
    ops = re.compile(r'mul\((\d+),(\d+)\)')

    result = 0
    for x, y in re.findall(ops, text):
        result += int(x) * int(y)
    ic(result)

    result = 0
    enabled = re.findall(r'''(?:(?<=do\(\))|^)(.*?)(?:(?=don't\(\))|$)''', text, flags=re.DOTALL)
    for x, y in re.findall(ops, ' '.join(enabled)):
        result += int(x) * int(y)
    ic(result)


if __name__ == '__main__':
    main()
