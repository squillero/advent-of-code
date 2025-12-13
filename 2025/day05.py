# Advent of Code 2025 | https://adventofcode.com/2025/day/5
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import namedtuple
from itertools import combinations
from icecream import ic

INPUT_FILE_NAME = 'day05-test.txt'
INPUT_FILE_NAME = 'day05-input.txt'

Range = namedtuple('Range', ['s', 'e'])


def main():
    with open(INPUT_FILE_NAME) as file:
        ranges_raw, ingredient_raw = file.read().split('\n\n')

    # Part1: An excercise on list comprehension & generators
    ranges = {Range(*map(int, line.split('-'))) for line in ranges_raw.split()}
    ingredients = [int(i) for i in ingredient_raw.split()]
    fresh_count = sum(any(rs <= i <= re for rs, re in ranges) for i in ingredients)
    ic(fresh_count)

    # Part2: Join & prune ranges
    stable = False
    while not stable:
        for s1, s2 in combinations(sorted(ranges), r=2):
            if s1.s <= s2.s <= s1.e <= s2.e:
                # ie. <1 <2 1> 2>
                ranges.remove(s1)
                ranges.remove(s2)
                ranges.add(Range(s1.s, s2.e))
                break
            elif s1.s <= s2.s <= s2.e <= s1.e:
                # ie. <1 <2 2> 1>
                ranges.remove(s2)
                break
        else:
            stable = True
    num_fresh = 0
    for s, e in ranges:
        num_fresh += e - s + 1
    ic(num_fresh)


if __name__ == '__main__':
    main()
