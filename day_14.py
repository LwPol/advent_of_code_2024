import re
import itertools
from typing import NamedTuple
from collections import deque


ROBOT_CONFIG_REGEX = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')

MAP_SIZE = (101, 103)

class Robot(NamedTuple):
    position: tuple[int, int]
    velocity: tuple[int, int]


def parse_robots_positions(lines: list[str]) -> list[Robot]:
    def parse_line(line: str) -> Robot:
        x, y, vx, vy = ROBOT_CONFIG_REGEX.match(line).groups()
        return Robot(position=(int(x), int(y)), velocity=(int(vx), int(vy)))
    return [parse_line(line) for line in lines]


def move_robot(robot: Robot, time: int) -> tuple[int, int]:
    x, y = robot.position
    vx, vy = robot.velocity
    return ((x + time * vx) % MAP_SIZE[0], (y + time * vy) % MAP_SIZE[1])


def move_robots(robots: list[Robot], time: int) -> list[tuple[int, int]]:
    return [move_robot(r, time) for r in robots]


def calculate_safety_factor(robots: list[Robot], time: int) -> int:
    mid_x = MAP_SIZE[0] // 2
    mid_y = MAP_SIZE[1] // 2
    nw, ne, sw, se = (0, 0, 0, 0)
    for x, y in move_robots(robots, time):
        if x < mid_x and y < mid_y:
            nw += 1
        elif x > mid_x and y < mid_y:
            ne += 1
        elif x < mid_x and y > mid_y:
            sw += 1
        elif x > mid_x and y > mid_y:
            se += 1
    return nw * ne * sw * se


def is_on_map(point: tuple[int, int]) -> bool:
    x, y = point
    return x >= 0 and x < MAP_SIZE[0] and y >= 0 and y < MAP_SIZE[1]


def get_closest_robot_distance(positions: set[tuple[int, int]],
                               point: tuple[int, int]) -> int:
    dxs = (-1, 0, 1, 1, 1, 0, -1, -1)
    dys = (-1, -1, -1, 0, 1, 1, 1, 0)
    queue = deque([(point, 0)])
    visited = set()
    while queue:
        elem, distance = queue.popleft()
        if distance > 0 and elem in positions:
            return distance
        if elem in visited:
            continue
        
        visited.add(elem)
        x, y = elem
        for dx, dy in zip(dxs, dys):
            next_pos = (x + dx, y + dy)
            if is_on_map(next_pos) and next_pos not in visited:
                queue.append((next_pos, distance + 1))
    raise RuntimeError('Other robot not found')


def get_cluster_indication(positions: list[tuple[int, int]]) -> float:
    pos_set = set(positions)
    s = sum(get_closest_robot_distance(pos_set, pt) for pt in positions)
    return s / len(positions)


def enumerate_plausible_candidates(robots: list[Robot], max_time: int):
    threshold = 2.0
    for i in range(1, max_time):
        robot_positions = move_robots(robots, time=i)
        cluster_ind = get_cluster_indication(robot_positions)
        if cluster_ind < threshold:
            yield i, set(robot_positions)


def map_out_region(robots: set[tuple[int, int]],
                   point: tuple[int, int]) -> set[tuple[int, int]]:
    dxs = (0, 1, 0, -1)
    dys = (-1, 0, 1, 0)
    def dfs(current: tuple[int, int], region: set[tuple[int, int]]):
        x, y = current
        for dx, dy in zip(dxs, dys):
            next_pos = (x + dx, y + dy)
            if is_on_map(next_pos) and next_pos not in region and next_pos in robots:
                region.add(next_pos)
                dfs(next_pos, region)
    region = {point}
    dfs(point, region)
    return region


def collect_regions(robots: set[tuple[int, int]],
                    size_threshold: int) -> list[set[tuple[int, int]]]:
    rest = set(robots)
    result = []
    while rest:
        region = map_out_region(robots, next(iter(rest)))
        rest -= region
        if len(region) >= size_threshold:
            result.append(region)
    result.sort(key=len, reverse=True)
    return result


def is_region_symmetrical(region: set[tuple[int, int]]) -> bool:
    def is_mirrored(point: tuple[int, int], axis: int) -> bool:
        x, y = point
        return (2 * axis - x, y) in region
    x_min = min(x for (x, _) in region)
    x_max = max(x for (x, _) in region)
    x_mid = (x_min + x_max) / 2
    return all(is_mirrored(pt, x_mid) for pt in region)


def check_candidate(robots: set[tuple[int, int]]) -> bool:
    rs = collect_regions(robots, size_threshold=10)
    return rs and is_region_symmetrical(rs[0])


def dump_robots_positions(robots: set[tuple[int, int]]):
    grid = [list(itertools.repeat('.', MAP_SIZE[0])) for _ in range(MAP_SIZE[1])]
    for x, y in robots:
        grid[y][x] = '#'
    for row in grid:
        print(''.join(row))


def find_plausible_christmas_tree_combination(robots: list[Robot]) -> int:
    for time, positions_set in enumerate_plausible_candidates(robots, max_time=20000):
        if check_candidate(positions_set):
            dump_robots_positions(positions_set)
            return time
    raise RuntimeError('Probably we should not be here')


def resolve_part1(input):
    return calculate_safety_factor(parse_robots_positions(input), time=100)

def resolve_part2(input):
    return find_plausible_christmas_tree_combination(parse_robots_positions(input))
