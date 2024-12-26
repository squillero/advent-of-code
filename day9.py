# Advent of Code 2024 | https://adventofcode.com/2024/day/9
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import deque, namedtuple
from tqdm.auto import tqdm
from icecream import ic


# INPUT_FILE = 'day9-example.txt'
INPUT_FILE = 'day9-input.txt'

Chunk = namedtuple('Chunk', ['id', 'start', 'len'])

EMPTY_BLOCK = -1


def read_layout(filename):
    full_layout = list()
    files = list()
    spaces = list()

    file_id = 0
    for idx, block in enumerate(open(filename).read().strip()):
        block = int(block)
        if idx % 2 == 0:
            files.append(Chunk(file_id, len(full_layout), block))
            full_layout.extend([file_id] * block)
            file_id += 1
        else:
            spaces.append(Chunk(EMPTY_BLOCK, len(full_layout), block))
            full_layout.extend([EMPTY_BLOCK] * block)
    return full_layout, files, spaces


def print_layout(layout):
    layout = ''.join('.' if c < 0 else str(c) for c in layout)
    ic(layout)


def main():
    original_layout, original_files, original_spaces = read_layout(INPUT_FILE)

    # --- Part One ---
    new_layout = original_layout[:]
    spaces = deque(i for i, b in enumerate(new_layout) if b == EMPTY_BLOCK)
    files = deque(i for i, b in enumerate(new_layout) if b != EMPTY_BLOCK)
    while spaces[0] < files[EMPTY_BLOCK]:
        new_layout[spaces.popleft()] = new_layout[files[EMPTY_BLOCK]]
        new_layout[files.pop()] = EMPTY_BLOCK
    checksum = sum(pos * idx for pos, idx in enumerate(new_layout) if idx != EMPTY_BLOCK)
    ic(checksum)

    # --- Part Two ---
    new_layout = original_layout[:]
    files = original_files
    spaces = original_spaces
    for file in reversed(files):
        if (
            pos := next((i for i, s in enumerate(spaces) if s.len >= file.len), None)
        ) is not None and spaces[pos].start < file.start:
            free_block = spaces[pos]
            new_layout[free_block.start : free_block.start + file.len] = [file.id] * file.len
            new_layout[file.start : file.start + file.len] = [EMPTY_BLOCK] * file.len
            spaces[pos] = Chunk(EMPTY_BLOCK, free_block.start + file.len, free_block.len - file.len)
            assert spaces[pos].len >= 0
    checksum = sum(pos * idx for pos, idx in enumerate(new_layout) if idx != EMPTY_BLOCK)
    ic(checksum)


if __name__ == '__main__':
    main()
