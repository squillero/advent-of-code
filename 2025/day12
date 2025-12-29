# Advent of Code 2025 | https://adventofcode.com/2025/day/12
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from typing import Any

from copy import copy
from itertools import product
from collections import namedtuple
import re
import numpy as np

from tqdm.auto import tqdm
from icecream import ic

INPUT_FILE_NAME = 'day12-test.txt'
# INPUT_FILE_NAME = 'day12-input.txt'

Position = namedtuple('Position', ['row', 'col'])
Problem = namedtuple('Problem', ['size', 'presents'])


class Shape:
    _pattern: np.ndarray

    def __init__(self, pattern: Any) -> None:
        if isinstance(pattern, np.ndarray):
            self._pattern = pattern.copy()
        else:
            self._pattern = np.array(
                [[1 if d == '#' else 0 for d in list(r.strip())] for r in pattern.split()],
                dtype=int,
            )

    def rotate(self, ticks: int) -> Shape:
        return Shape(np.rot90(self._pattern, k=-ticks))

    @property
    def dim(self) -> tuple[int, int]:
        return self._pattern.shape

    @property
    def pattern(self) -> np.ndarray:
        return self._pattern


class Canvas:
    _canvas: np.ndarray

    def __init__(self, size) -> None:
        self._canvas = np.zeros(size, dtype=int)

    @property
    def canvas(self) -> np.ndarray:
        return self._canvas

    @property
    def dim(self):
        return self._canvas.shape

    def erase(self):
        self._canvas.fill(0)

    def single_stroke(self, pos: Position, brush: Shape) -> None:
        brush_rows, brush_cols = brush.dim
        self._canvas[
            pos.row : pos.row + brush_rows, pos.col : pos.col + brush_cols
        ] += brush.pattern

    def paint(self, strokes: list[tuple[Position, Shape]]) -> np.ndarray:
        self.erase()
        for pos, brush in strokes:
            self.single_stroke(pos, brush)
        return self._canvas


def read_problem(filename: str) -> list[Problem]:
    with open(filename) as file:
        presents_raw, regions_raw = file.read().rsplit('\n\n', maxsplit=1)
        presents_raw += '\n\n'  # patch

    presents = list()
    pattern = re.compile(r'(?P<num>\d+):$\n(?P<shape>(?:^[\.#]+$\n)+)\n', re.MULTILINE)
    for m in pattern.finditer(presents_raw):
        assert int(m.group('num')) == len(presents)  # paranoia check
        presents.append(Shape(m.group('shape')))
    problems = list()
    for line in regions_raw.rstrip().split('\n'):
        dim, rest = line.split(':')
        num_rows, dum_cols = map(int, dim.split('x'))
        selected = list()
        for i, m in enumerate(map(int, rest.split())):
            selected.extend([presents[i]] * m)
        problems.append(Problem((num_rows, dum_cols), tuple(selected)))

    return problems


def fit_shapes(
    space: Canvas, shapes: list[Shape], fitted: list[tuple[Position, Shape]]
) -> list[tuple[Position, Shape]]:
    if not shapes:
        return fitted
    # new_shapes = list(shapes)
    new_shapes = shapes
    p = new_shapes.pop()
    for row, col, rot in product(
        range(space.dim[0] - p.dim[0] + 1), range(space.dim[1] - p.dim[0] + 1), range(4)
    ):
        strokes = fitted + [(Position(row, col), p.rotate(rot))]
        if space.paint(strokes).max() > 1:
            continue
        solution = fit_shapes(space, new_shapes, strokes)
        if solution:
            return solution
    new_shapes.append(p)
    return list()


def main():
    problems = read_problem(INPUT_FILE_NAME)

    for problem in tqdm(problems):
        canvas = Canvas(problem.size)
        solution = fit_shapes(canvas, list(problem.presents), list())


if __name__ == '__main__':
    main()
