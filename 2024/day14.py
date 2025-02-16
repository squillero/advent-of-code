# Advent of Code 2024 | https://adventofcode.com/2024/day/14
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import namedtuple
from operator import mul
from functools import reduce
import re
import numpy as np
from tqdm.auto import tqdm
from icecream import ic

# INPUT_FILE = 'day14-example.txt'
INPUT_FILE = 'day14-input.txt'
# INPUT_FILE = 'day14-debug.txt'

SPACE_WIDTH = 101
SPACE_HEIGHT = 103

Robot = namedtuple('Robot', ['x', 'y', 'vx', 'vy'])


def read_robots(filename):
    r"""Read robots position and velocity"""
    robot_status = r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)'
    return [Robot(*map(int, n)) for n in re.findall(robot_status, open(filename).read())]


def robot_step(robot):
    r"""Perform 1 step fo the robot"""
    return Robot(
        x=(robot.x + SPACE_WIDTH + robot.vx) % SPACE_WIDTH,
        y=(robot.y + SPACE_HEIGHT + robot.vy) % SPACE_HEIGHT,
        vx=robot.vx,
        vy=robot.vy,
    )


def main():
    robots_init = read_robots(INPUT_FILE)

    # --- Part One ---
    robots = list(robots_init)
    for _ in tqdm(range(100)):
        robots = map(robot_step, robots)

    q = [0, 0, 0, 0]
    for r in robots:
        if 0 <= r.x < SPACE_WIDTH // 2 and 0 <= r.y < SPACE_HEIGHT // 2:
            q[0] += 1
        elif r.x >= SPACE_WIDTH - SPACE_WIDTH // 2 and 0 <= r.y < SPACE_HEIGHT // 2:
            q[1] += 1
        elif 0 <= r.x < SPACE_WIDTH // 2 and r.y >= SPACE_HEIGHT - SPACE_HEIGHT // 2:
            q[2] += 1
        elif r.x >= SPACE_WIDTH - SPACE_WIDTH // 2 and r.y >= SPACE_HEIGHT - SPACE_HEIGHT // 2:
            q[3] += 1

    safety_factor = reduce(mul, q)
    ic(safety_factor)

    # --- Part Two ---
    robots = list(robots_init)
    steps = 0
    with tqdm() as pbar:
        while True:
            m = np.full((SPACE_HEIGHT, SPACE_WIDTH), ' ')
            for r in robots:
                m[SPACE_HEIGHT - 1 - r.y, r.x] = '#'

            if any('#' * 10 in ''.join(m[i]) for i in range(SPACE_HEIGHT)) and any(
                '#' * 10 in ''.join(m.T[i]) for i in range(SPACE_WIDTH)
            ):
                # A pattern with a line and a column BOTH with 10 conscutive #'s!?
                for r in range(SPACE_HEIGHT):
                    print(''.join(m[SPACE_HEIGHT - 1 - r, c] for c in range(SPACE_WIDTH)))
                break

            robots = list(map(robot_step, robots))
            steps += 1
            pbar.update(1)
    ic(steps)


if __name__ == '__main__':
    main()
