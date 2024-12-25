# Copyright 2024 by Giovanni Squillero
# SPDX-License-Identifier: 0BSD

from itertools import pairwise
from icecream import ic

INPUT_FILE = 'day2-input.txt'


def check_report_safety(report):
    r"""Test wether `report` is safe"""
    return all(1 <= abs(e1 - e2) <= 3 for e1, e2 in pairwise(report)) and (
        report == sorted(report) or report == sorted(report, reverse=True)
    )


def main():
    safe_count_1 = 0
    safe_count_2 = 0
    try:
        with open(INPUT_FILE) as file:
            for line in file:
                report = [int(r) for r in line.split()]

                safe = check_report_safety(report)
                safe_count_1 += safe

                candidate_reports = (report[:i] + report[i + 1 :] for i in range(len(report)))
                safe_count_2 += safe or any(check_report_safety(r) for r in candidate_reports)

    except OSError as problem:
        exit(problem)
    ic(safe_count_1)
    ic(safe_count_2)


if __name__ == '__main__':
    main()
