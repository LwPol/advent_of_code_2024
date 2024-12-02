import itertools
from typing import Optional


def parse_reports(lines: list[str]) -> list[list[int]]:
    return [[int(num) for num in line.split()] for line in lines]


def find_bad_level_index(report: list[int]) -> Optional[int]:
    if len(report) < 2:
        return None
    
    should_increase = report[0] < report[1]
    lower_limit = 1 if should_increase else -3
    upper_limit = 3 if should_increase else -1
    def is_good_level(elem) -> bool:
        x, y = elem[1]
        return lower_limit <= y - x <= upper_limit
    it = itertools.filterfalse(is_good_level, enumerate(itertools.pairwise(report)))
    ret = next(it, None)
    return ret[0] if ret is not None else None


def is_safe(report: list[int]) -> bool:
    if len(report) < 2:
        return None
    
    should_increase = report[0] < report[1]
    lower_limit = 1 if should_increase else -3
    upper_limit = 3 if should_increase else -1
    return all(lower_limit <= y - x <= upper_limit for x, y in itertools.pairwise(report))


def count_safe_reports(reports: list[list[int]]) -> int:
    return sum(1 for r in reports if is_safe(r))


def is_safe_enough(report: list[int]) -> bool:
    if is_safe(report):
        return True
    return any(is_safe(report[:i] + report[i + 1:]) for i in range(len(report)))


def count_safe_reports_with_tolerance(reports: list[list[int]]) -> int:
    return sum(1 for r in reports if is_safe_enough(r))


def resolve_part1(input):
    return count_safe_reports(parse_reports(input))

def resolve_part2(input):
    return count_safe_reports_with_tolerance(parse_reports(input))
