# Advent of Code 2024 | https://adventofcode.com/2024/day/13
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from math import sqrt
import re
from collections import namedtuple, Counter
from itertools import count, chain
from tqdm.auto import tqdm
from icecream import ic

# INPUT_FILE = 'day13-example_small.txt'
INPUT_FILE = 'day13-input.txt'


State = namedtuple('State', ['x', 'y', 'tok'])
Buttons = namedtuple('Buttons', ['a', 'b'])


def read_problems(filename):
    raw_text = open(filename).read()
    problem = r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)'
    return [
        (
            State(x=int(nums[4]), y=int(nums[5]), tok=None),
            Buttons(
                a=State(x=int(nums[0]), y=int(nums[1]), tok=3),
                b=State(x=int(nums[2]), y=int(nums[3]), tok=1),
            ),
        )
        for nums in re.findall(problem, raw_text)
    ]


def a_star(target, buttons):
    r"""Vanilla A* algorithm"""
    fronteer = [State(x=0, y=0, tok=0)]

    cost_x = min(a.tok / a.x for a in buttons)
    cost_y = min(a.tok / a.y for a in buttons)

    def c(s):
        return s.tok

    def h(s):
        return (target.x - s.x) * cost_x + (target.y - s.y) * cost_y

    visited = set()
    while fronteer:
        s = fronteer.pop()
        visited.add(s)
        if s.x == target.x and s.y == target.y:
            return s.tok
        for b in buttons:
            ns = State(x=s.x + b.x, y=s.y + b.y, tok=s.tok + b.tok)
            if ns not in visited and ns.x <= target.x and ns.y <= target.y:
                fronteer.append(ns)
        fronteer.sort(
            key=lambda s: c(s) + h(s),
            reverse=True,
        )
    return 0


def fillable(tot_x, tot_y, sx, sy):
    r"""Checks whether `tot` can be reached with steps `s`"""
    return tot_x % sx == 0 and tot_y % sy == 0 and tot_x // sx == tot_y // sy


def fill_and_swap(target, filler, swap):
    r"""Puts as many `filler` possible, then complete swapping them with `swap`"""
    tx, ty = target
    fx, fy = filler
    sx, sy = swap
    num_swaps, num_fills = next(
        (
            ((tx - fx * num_fills) // sx, num_fills)
            for num_fills in range(min(tx // fx, ty // fy) + 1)
            if fillable(tx - fx * num_fills, ty - fy * num_fills, sx, sy)
        ),
        (0, 0),
    )
    return num_fills, num_swaps


def main():
    problems = read_problems(INPUT_FILE)

    # --- Part One (scholastic) ---
    tokens = 0
    for target, buttons in tqdm(problems):
        tokens += a_star(target, buttons)
    ic(tokens)

    # --- Part One (faster, problem specific) ---
    tokens = 0
    for target, buttons in tqdm(problems):
        a1, b1 = fill_and_swap(
            (target.x, target.y), (buttons.a.x, buttons.a.y), (buttons.b.x, buttons.b.y)
        )
        if a1 and b1:
            b2, a2 = fill_and_swap(
                (target.x, target.y), (buttons.b.x, buttons.b.y), (buttons.a.x, buttons.a.y)
            )
        else:
            a2, b2 = 0, 0
        tokens += min(a1 * 3 + b1, a2 * 3 + b2)
    ic(tokens)

    # --- Part Two ---
    OFFSET = 10_000_000_000_000
    tokens = 0
    for target, buttons in tqdm(problems):
        target = State(target.x + OFFSET, target.y + OFFSET, target.tok)
        a1, b1 = fill_and_swap(
            (target.x, target.y), (buttons.a.x, buttons.a.y), (buttons.b.x, buttons.b.y)
        )
        ic(a1, b1)
        if a1 and b1:
            b2, a2 = fill_and_swap(
                (target.x, target.y), (buttons.b.x, buttons.b.y), (buttons.a.x, buttons.a.y)
            )
        else:
            a2, b2 = 0, 0
        ic(a2, b2)
        tokens += min(a1 * 3 + b1, a2 * 3 + b2)

    ic(tokens)


if __name__ == '__main__':
    main()
