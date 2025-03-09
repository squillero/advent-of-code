# Advent of Code 2024 | https://adventofcode.com/2024/day/5
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import namedtuple
from itertools import accumulate
from functools import partial
import re
from icecream import ic

# INPUT_FILE = 'day05-example.txt'
INPUT_FILE = 'day05-input.txt'

Rule = namedtuple('Rule', ['before', 'after'])


def read_problem_definition(filename):
    r"""Lazy parse of input file using regex"""
    text = open(filename).read()
    rules = list()
    for b, a in re.findall(r'(\d+)\|(\d+)\n', text):
        rules.append(Rule(int(b), int(a)))
    updates = list()
    for line in re.findall(r'(^(?:\d+,)*\d+)$', text, flags=re.MULTILINE):
        updates.append([int(p) for p in line.split(',')])
    return rules, updates


def check_update(sequence, rules):
    r"""Check a single update sequence against a ruleset"""
    for r in rules:
        if (
            r.before in sequence
            and r.after in sequence
            and sequence.index(r.before) > sequence.index(r.after)
        ):
            return False
    return True


def add_page_to_sequence(sequence, page, rules):
    r"""Insert `page` into `sequence` in the first valid position -- O(len(seq))"""
    candidates = (sequence[:i] + [page] + sequence[i:] for i in range(len(sequence) + 1))
    return next(filter(partial(check_update, rules=rules), candidates))


def main():
    rules, updates = read_problem_definition(INPUT_FILE)

    # --- Part One ---
    correct_updates = filter(partial(check_update, rules=rules), updates)
    checksum = sum(u[len(u) // 2] for u in correct_updates)
    ic(checksum)

    # --- Part Two ---
    correct_sequences = list()
    for wrong in filter(lambda s: not check_update(s, rules), updates):
        *_, correct = accumulate(
            wrong, partial(add_page_to_sequence, rules=rules), initial=list()
        )
        correct_sequences.append(correct)
    checksum = sum(u[len(u) // 2] for u in correct_sequences)
    ic(checksum)


if __name__ == '__main__':
    main()
