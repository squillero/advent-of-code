# Advent of Code 2025 | https://adventofcode.com/2025/day/10
# Copyright 2025 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from typing import Iterable
from itertools import combinations, combinations_with_replacement
import re
from tqdm.auto import tqdm

from icecream import ic

INPUT_FILE_NAME = 'day10-test.txt'
# INPUT_FILE_NAME = 'day10-input.txt'


class Machine:
    """A machine."""

    # see: https://docs.python.org/3/library/typing.html#annotating-tuples
    _button_wirings: tuple[tuple[int, ...], ...]
    _goal_light: tuple[bool, ...]
    _goal_joltage: tuple[int, ...]

    def __init__(self, diagram, buttons, joltage):
        tmp = list()
        for b in buttons.split():
            tmp.append(tuple(map(int, b[1:-1].split(','))))
        self._button_wirings = tuple(tmp)
        self._goal_light = tuple(l == '#' for l in diagram.strip())
        self._goal_joltage = tuple(map(int, joltage.split(',')))

    @property
    def goal_light(self) -> tuple[bool, ...]:
        return self._goal_light

    @property
    def goal_joltage(self) -> tuple[int, ...]:
        return self._goal_joltage

    @property
    def num_buttons(self) -> int:
        return len(self._button_wirings)

    def __str__(self) -> str:
        return f'[{self.goal_light}] {" ".join(str(_) for _ in self._button_wirings)} {{{self._goal_joltage}}}'

    def press_buttons(self, buttons: Iterable[int]):
        """Reset machine, then set status by pressing a sequence of buttons."""
        status = [False] * len(self._goal_light)
        for button in buttons:
            for w in self._button_wirings[button]:
                status[w] = not status[w]
        return tuple(status)

    def press_buttons_joltage(self, buttons: Iterable[int]):
        """Reset machine, then set status by pressing a sequence of buttons."""
        status = [0] * len(self._goal_light)
        for button in buttons:
            for w in self._button_wirings[button]:
                status[w] += 1
        return tuple(status)


def main():
    pattern = re.compile(r'\[(?P<diagram>.*)\]\s*(?P<buttons>.*)\s*\{(?P<joltage>.*)\}')

    machines = list()
    with open(INPUT_FILE_NAME) as file:
        for line in file:
            assert (m := pattern.match(line))
            machines.append(Machine(m.group('diagram'), m.group('buttons'), m.group('joltage')))

    # = [Part 1] ============================================================
    # Simple brute force
    checksum = 0
    for machine in tqdm(machines):
        goal = machine.goal_light
        for length in range(1, machine.num_buttons + 1):
            if any(
                machine.press_buttons(buttons) == goal
                for buttons in combinations(range(machine.num_buttons), length)
            ):
                checksum += length
                break
        else:
            assert False
    ic(checksum)

    # = [Part 2] ============================================================
    # Part 2 -- As previous, but with a different goal (joltage)

    checksum = 0
    for machine in machines:
        goal = machine.goal_joltage
        reasonable_buttons = list()
        for button in range(machine.num_buttons):
            tmp = list()
            while all(c < g for c, g in zip(machine.press_buttons_joltage(tmp), goal)):
                tmp.append(button)
            reasonable_buttons.extend(tmp)

        # Notez Bien: The total number of combinations of "reasonable" buttons
        # would be something like (rough estimated):
        # 1,050,932,584,007,919,465,924,231,680,174,062,991,803,882,860,871,821,049
        #   507,210,975,344,873,147,865,476,054,520,905,922,902,746,390,892,555,684
        #   070,111,906,482,732,065,067,261,496,208,661,405,117,413,289,190,368,364
        #   266,394,710,981,301,717,346,962,896,309,115,085,260,012,484,310,087,905
        #   036,909,879,433,459,334,968,606,976,080,067,869,701,628,670,691,652,990
        #   372,309,557,477,009,209,344,293,463,511,528,898,666,754,457,810,242,512
        #   444,774,202,470,900,723,464,559,433,806,252 ;-)

        checksum += try_joltage(machine, reasonable_buttons)

    ic(checksum)


def try_joltage(machine, reasonable_buttons):

    goal = machine.goal_joltage
    best_solution = reasonable_buttons[:]
    mask = [False] * len(reasonable_buttons)

    def _try_joltage(pos):
        if sum(mask) > len(best_solution):
            return 0
        buttons = [b for b, m in zip(reasonable_buttons, mask) if m]
        joltage = machine.press_buttons_joltage(buttons)
        if joltage == goal and sum(mask) < len(best_solution):
            best_solution[:] = buttons[:]
            ic(len(best_solution), best_solution)
            return 1
        elif any(c > g for c, g in zip(joltage, goal)):
            return 0
        elif pos >= len(reasonable_buttons):
            return 0
        mask[pos] = True
        _try_joltage(pos + 1)
        mask[pos] = False
        _try_joltage(pos + 1)

    _try_joltage(0)
    return len(best_solution)


if __name__ == '__main__':
    main()
