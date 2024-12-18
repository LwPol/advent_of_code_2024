from collections import deque
from typing import Optional

Point = tuple[int, int]

GRID_SIZE = 71


def parse_bytes_positions(lines: list[str]) -> list[Point]:
    def parse_line(line: str) -> Point:
        x, y = line.split(',')
        return int(x), int(y)
    return list(map(parse_line, lines))


def is_on_grid(point: Point) -> bool:
    x, y = point
    return x >= 0 and x < GRID_SIZE and y >= 0 and y < GRID_SIZE


def get_neighbours(point: Point) -> [Point]:
    x, y = point
    dxs = (1, 0, -1, 0)
    dys = (0, 1, 0, -1)
    neighbours = [(x + dx, y + dy) for dx, dy in zip(dxs, dys)]
    return list(filter(is_on_grid, neighbours))


def get_distance_to_exit(byte_positions: list[Point]) -> Optional[int]:
    start = (0, 0)
    target = (GRID_SIZE - 1, GRID_SIZE - 1)

    queue = deque([(start, 0)])
    recorded = {start}
    bytes_set = set(byte_positions)
    while queue:
        point, distance = queue.popleft()
        if point == target:
            return distance

        for neigh in get_neighbours(point):
            if neigh not in recorded and neigh not in bytes_set:
                queue.append((neigh, distance + 1))
                recorded.add(neigh)
    return None


def is_end_reachable(bytes_positions: list[Point]) -> bool:
    return get_distance_to_exit(bytes_positions) is not None


def binary_search(bytes_positions: list[Point], lower_bound: int, upper_bound: int) -> int:
    if upper_bound - lower_bound == 1:
        return upper_bound
    
    mid = (lower_bound + upper_bound) // 2
    if is_end_reachable(bytes_positions[:mid]):
        return binary_search(bytes_positions, mid, upper_bound)
    return binary_search(bytes_positions, lower_bound, mid)


def resolve_part1(input):
    bytes_positions = parse_bytes_positions(input)
    return get_distance_to_exit(bytes_positions[:1024])

def resolve_part2(input):
    bytes_positions = parse_bytes_positions(input)
    block_count = binary_search(bytes_positions, 1024, len(bytes_positions))
    x, y = bytes_positions[block_count - 1]
    return f'{x},{y}'
