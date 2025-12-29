# Advent of Code 2025 | https://adventofcode.com/2025/day/8
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import Counter, namedtuple
from functools import reduce
from itertools import combinations
from operator import mul
import logging
from tqdm.auto import tqdm
from icecream import ic

INPUT_FILE_NAME = 'day08-test.txt'
MAX_CONNECTIONS = 10

# INPUT_FILE_NAME = 'day08-input.txt'
# MAX_CONNECTIONS = 1_000


JunctionBox = namedtuple('JunctionBox', ['x', 'y', 'z'])


def d(j1: JunctionBox, j2: JunctionBox) -> float:
    """Calculate distance between two junctions"""
    return ((j1.x - j2.x) ** 2 + (j1.y - j2.y) ** 2 + (j1.z - j2.z) ** 2) ** 0.5


# Idea: circuit's id == smallest jbox's id in the circuit (jboxes[x]).
def join_circuits(jboxes: dict[JunctionBox, int], j1: JunctionBox, j2: JunctionBox):
    """Join circuits j1 and j2"""

    if jboxes[j1] == jboxes[j2]:
        return  # not really needed, but maybe a little bit faster
    new_circuit = min(jboxes[j1], jboxes[j2])
    old_circuit = max(jboxes[j1], jboxes[j2])
    # merge two circuits
    for j, v in jboxes.items():
        if v == old_circuit:
            jboxes[j] = new_circuit


def main():
    with open(INPUT_FILE_NAME) as file:
        jboxes = {JunctionBox(*map(int, line.split(','))): 0 for line in file}

    # List of all junction pairs, sorted by distance.
    sorted_junctions = sorted(
        ((j1, j2) for j1, j2 in combinations(jboxes.keys(), r=2)), key=lambda j: d(*j)
    )

    # = [Part 1] ==================================================================================
    for n, k in enumerate(jboxes.keys()):
        jboxes[k] = n + 1  # reset circuits
    for j1, j2 in sorted_junctions[:MAX_CONNECTIONS]:
        join_circuits(jboxes, j1, j2)
    cnt = Counter(jboxes.values())
    ic(cnt.most_common(3))
    check = reduce(mul, (v for _, v in cnt.most_common(3)), 1)
    ic(check)

    # = [Part 2] ==================================================================================
    for n, k in enumerate(jboxes.keys()):
        jboxes[k] = n + 1  # reset circuits
    while len(set(jboxes.values())) > 1:
        j1, j2 = sorted_junctions.pop(0)
        join_circuits(jboxes, j1, j2)
    ic(j1.x * j2.x)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    main()
