from collections import defaultdict
from typing import Callable
import itertools

Point = tuple[int, int]
AntennasMap = dict[str, list[Point]]
AntinodesFunc = Callable[[list[str], Point, Point], list[Point]]

def collect_antennas_positions(grid: list[str]) -> AntennasMap:
    result = defaultdict(list)
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != '.':
                result[c].append((x, y))
    return result


def is_in_range(grid: list[str], pos: Point) -> bool:
    x, y = pos
    width = len(grid[0])
    height = len(grid)
    return x >= 0 and x < width and y >= 0 and y < height


def get_antinodes(grid: list[str], pos1: Point, pos2: Point) -> list[Point]:
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    p1 = (pos2[0] + dx, pos2[1] + dy)
    p2 = (pos1[0] - dx, pos1[1] - dy)
    return list(filter(lambda p: is_in_range(grid, p), [p1, p2]))


def collect_antinodes(grid: list[str],
                      antennas: list[Point],
                      antinodes_generator: AntinodesFunc) -> set[Point]:
    antinodes = set()
    for a1, a2 in itertools.combinations(antennas, r=2):
        antinodes.update(antinodes_generator(grid, a1, a2))
    return antinodes


def count_all_antinodes(grid: list[str], antinodes_generator: AntinodesFunc):
    antennas = collect_antennas_positions(grid)
    antinodes = set()
    for freq, positions in antennas.items():
        antinodes.update(collect_antinodes(grid, positions, antinodes_generator))
    return len(antinodes)


def get_antinodes_p2(grid: list[str], pos1: Point, pos2: Point) -> list[Point]:
    result = [pos1, pos2]
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    antinode = (pos2[0] + dx, pos2[1] + dy)
    while is_in_range(grid, antinode):
        result.append(antinode)
        antinode = (antinode[0] + dx, antinode[1] + dy)
    antinode = (pos1[0] - dx, pos1[1] - dy)
    while is_in_range(grid, antinode):
        result.append(antinode)
        antinode = (antinode[0] - dx, antinode[1] - dy)
    return result


def resolve_part1(input):
    return count_all_antinodes(input, get_antinodes)

def resolve_part2(input):
    return count_all_antinodes(input, get_antinodes_p2)
