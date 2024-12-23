# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

import logging
import re
from icecream import ic

INPUT_FILE = 'day3-example.txt'
INPUT_FILE = 'day3-input.txt'


def slurp(filename):
    r"""Slurp the whole file"""
    try:
        with open(filename) as file:
            return file.read()
    except OSError as problem:
        logging.error(f'slurp: {problem}')
        return ''


def main():
    r"""Standard entry point"""

    text = slurp(INPUT_FILE)
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
