import itertools
from collections import deque
from typing import Optional, Callable, Iterator


Point = tuple[int, int]
CheatEnumerator = Callable[[list[str]], Iterator[int]]


def get_char_at(grid: list[str], point: Point) -> str:
    x, y = point
    return grid[y][x]


def find_position(grid: list[str], value: str) -> Point:
    width = len(grid[0])
    height = len(grid)
    return next(pt for pt in itertools.product(range(width), range(height))
                if get_char_at(grid, pt) == value)


def get_neighbours(point: Point) -> [Point]:
    dxs = (1, 0, -1, 0)
    dys = (0, 1, 0, -1)
    x, y = point
    return [(x + dx, y + dy) for dx, dy in zip(dxs, dys)]


def create_target_distance_map(grid: list[str]) -> dict[Point, int]:
    target = find_position(grid, value='E')
    result = {target: 0}
    queue = deque([(target, 0)])
    while queue:
        node, distance = queue.popleft()
        for point in get_neighbours(node):
            if get_char_at(grid, point) == '#':
                continue
            if point not in result:
                new_distance = distance + 1
                result[point] = new_distance
                queue.append((point, new_distance))
    return result


def is_on_edge(grid: list[str], point: Point) -> bool:
    width = len(grid[0])
    height = len(grid)
    x, y = point
    return x == 0 or x == width - 1 or y == 0 or y == height - 1


def get_direction(point1: Point, point2: Point) -> tuple[int, int]:
    return point2[0] - point1[0], point2[1] - point1[1]


def get_time_safe_for_cheat(grid: list[str],
                            distance_map: dict[Point, int],
                            current: Point,
                            wall: Point) -> Optional[int]:
    if is_on_edge(grid, wall):
        return None

    dx, dy = get_direction(current, wall)
    target_tile = (current[0] + 2 * dx, current[1] + 2 * dy)
    if get_char_at(grid, target_tile) == '#':
        return None
    save = distance_map[current] - distance_map[target_tile]
    return save - 2 if save > 2 else None


def find_cheats(grid: list[str]):
    distance_map = create_target_distance_map(grid)
    start = find_position(grid, 'S')
    visited = set()
    queue = deque([start])
    while queue:
        current = queue.popleft()
        visited.add(current)
        for neigh in get_neighbours(current):
            if get_char_at(grid, neigh) == '#':
                save = get_time_safe_for_cheat(grid, distance_map, current, neigh)
                if save is not None:
                    yield save
            elif neigh not in visited:
                queue.append(neigh)


def count_cheats_with_save_threshold(grid: list[str],
                                     cheat_func: CheatEnumerator,
                                     threshold: int) -> int:
    return sum(1 for cheat in cheat_func(grid) if cheat >= threshold)


def manhattan_distance(point1: Point, point2: Point) -> int:
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])


def find_extended_cheats(grid: list[str]):
    distance_map = create_target_distance_map(grid)
    for pt1, pt2 in itertools.combinations(distance_map.keys(), r=2):
        dist = manhattan_distance(pt1, pt2)
        if dist <= 20:
            time_save = abs(distance_map[pt1] - distance_map[pt2])
            if time_save > dist:
                yield time_save - dist


def resolve_part1(input):
    return count_cheats_with_save_threshold(input, find_cheats, threshold=100)

def resolve_part2(input):
    return count_cheats_with_save_threshold(input, find_extended_cheats, threshold=100)
