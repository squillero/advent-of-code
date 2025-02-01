# Advent of Code 2024 | https://adventofcode.com/2024/day/14
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from collections import namedtuple
from operator import mul
from functools import reduce
import re
from icecream import ic
from tqdm.auto import tqdm

# INPUT_FILE = 'day14-example.txt'
INPUT_FILE = 'day14-input.txt'

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
        x=(robot.x + robot.vx) % SPACE_WIDTH,
        y=(robot.y + robot.vy) % SPACE_HEIGHT,
        vx=robot.vx,
        vy=robot.vy,
    )


def main():
    robots = read_robots(INPUT_FILE)

    # --- Part One ---
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


if __name__ == '__main__':
    main()
