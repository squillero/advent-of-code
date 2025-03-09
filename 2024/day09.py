# Advent of Code 2024 | https://adventofcode.com/2024/day/9
# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import deque, namedtuple
from icecream import ic


# INPUT_FILE = 'day09-example.txt'
INPUT_FILE = 'day09-input.txt'

Chunk = namedtuple('Chunk', ['id', 'start', 'len'])

EMPTY_BLOCK = -1


def parse_layout(layout_description):
    r"""Expand layout description into explicit layout"""
    full_layout = list()

    file_id = 0
    for idx, block in enumerate(layout_description):
        block = int(block)
        if idx % 2 == 0:
            full_layout.extend([file_id] * block)
            file_id += 1
        else:
            full_layout.extend([EMPTY_BLOCK] * block)
    return full_layout


def build_lists(layout_description):
    r"""Builds lists of files and empty blocks"""
    files = list()
    spaces = list()
    file_id = 0
    pos = 0
    for idx, block in enumerate(layout_description):
        block_size = int(block)
        if idx % 2 == 0:
            files.append(Chunk(file_id, pos, block_size))
            file_id += 1
        else:
            spaces.append(Chunk(EMPTY_BLOCK, pos, block_size))
        pos += block_size
    return files, spaces


def main():
    layout_description = open(INPUT_FILE).read().strip()

    # --- Part One ---
    layout = parse_layout(layout_description)
    files = deque(i for i, b in enumerate(layout) if b != EMPTY_BLOCK)
    spaces = deque(i for i, b in enumerate(layout) if b == EMPTY_BLOCK)
    while spaces[0] < files[-1]:
        layout[spaces.popleft()] = layout[files[-1]]
        layout[files.pop()] = EMPTY_BLOCK
    checksum = sum(pos * idx for pos, idx in enumerate(layout) if idx != EMPTY_BLOCK)
    ic(checksum)

    # --- Part Two ---
    layout = parse_layout(layout_description)
    files, spaces = build_lists(layout_description)
    for file in reversed(files):
        if (
            pos := next((i for i, s in enumerate(spaces) if s.len >= file.len), None)
        ) is not None and spaces[pos].start < file.start:
            free_block = spaces[pos]
            layout[free_block.start : free_block.start + file.len] = [file.id] * file.len
            layout[file.start : file.start + file.len] = [EMPTY_BLOCK] * file.len
            spaces[pos] = Chunk(
                EMPTY_BLOCK, free_block.start + file.len, free_block.len - file.len
            )
    checksum = sum(pos * idx for pos, idx in enumerate(layout) if idx != EMPTY_BLOCK)
    ic(checksum)


if __name__ == '__main__':
    main()
