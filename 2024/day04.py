# Advent of Code 2024 | https://adventofcode.com/2024/day/4
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD


import numpy as np
from icecream import ic

TARGET = np.array(list('XMAS'))

# INPUT_FILE = 'day04-example.txt'
# INPUT_FILE = 'day04-example_dots2.txt'
INPUT_FILE = 'day04-input.txt'


def get_paths(station, pos):
    r"""Get plausible paths to look into"""
    max_r, max_c = station.shape
    r, c = pos
    paths = list()
    if r >= TARGET.size - 1:
        # North
        paths.append(([r - o for o in range(TARGET.size)], [c] * TARGET.size))
    if r >= TARGET.size - 1 and c <= max_c - TARGET.size:
        # North-East
        paths.append(
            ([r - o for o in range(TARGET.size)], [c + o for o in range(TARGET.size)])
        )
    if c <= max_c - TARGET.size:
        # East
        paths.append(([r] * TARGET.size, [c + o for o in range(TARGET.size)]))
    if r <= max_r - TARGET.size and c <= max_c - TARGET.size:
        # South-East
        paths.append(
            ([r + o for o in range(TARGET.size)], [c + o for o in range(TARGET.size)])
        )
    if r <= max_r - TARGET.size:
        # South
        paths.append(([r + o for o in range(TARGET.size)], [c] * TARGET.size))
    if r <= max_r - TARGET.size and c >= TARGET.size - 1:
        # South-West
        paths.append(
            ([r + o for o in range(TARGET.size)], [c - o for o in range(TARGET.size)])
        )
    if c >= TARGET.size - 1:
        # West
        paths.append(([r] * TARGET.size, [c - o for o in range(TARGET.size)]))
    if r >= TARGET.size - 1:
        # North-West
        paths.append(
            ([r - o for o in range(TARGET.size)], [c - o for o in range(TARGET.size)])
        )
    return paths


def get_paths_x(station, pos):
    r"""Get plausible path to look into for the X"""
    max_r, max_c = station.shape
    r, c = pos
    if r > 0 and r < max_r - 1 and c > 0 and c < max_c - 1:
        return [([r - 1, r - 1, r + 1, r + 1], [c - 1, c + 1, c - 1, c + 1])]
    else:
        return []


def main():
    station = np.array([list(line.rstrip()) for line in open(INPUT_FILE)])

    # --- Part One ---
    count = 0
    for r, c in zip(*np.where(station == 'X')):
        for path in get_paths(station, (r, c)):
            count += np.array_equal(station[path], TARGET)
    ic(count)

    # --- Part Two ---
    xcount = 0
    for r, c in zip(*np.where(station == 'A')):
        for path in get_paths_x(station, (r, c)):
            xcount += ''.join(station[path].tolist()) in {
                'MSMS',
                'SMSM',
                'MMSS',
                'SSMM',
            }
    ic(xcount)


if __name__ == '__main__':
    main()
