import itertools
from typing import Optional
from heapq import heappush, heappop

Point = tuple[int, int]
Direction = tuple[int, int]
Grid = list[str]

EAST = (1, 0)
WEST = (-1, 0)
NORTH = (0, -1)
SOUTH = (0, 1)


def get_grid_size(grid: Grid) -> tuple[int, int]:
    return len(grid[0]), len(grid)


def find_start_and_target(grid: Grid) -> tuple[Point, Point]:
    width, height = get_grid_size(grid)
    start = None
    target = None
    for x, y in itertools.product(range(width), range(height)):
        if grid[y][x] == 'S':
            start = (x, y)
        elif grid[y][x] == 'E':
            target = (x, y)
    return start, target


def enumerate_free_neighbours(grid: Grid, point: Point):
    x, y = point
    dxs = (1, 0, -1, 0)
    dys = (0, 1, 0, -1)
    neighbours = ((x + dx, y + dy) for dx, dy in zip(dxs, dys))
    return filter(lambda p: grid[p[1]][p[0]] != '#', neighbours)


def calc_direction(source: Point, target: Point) -> Direction:
    dx = target[0] - source[0]
    dy = target[1] - source[1]
    return dx, dy


def is_perpendicular(dir1: Direction, dir2: Direction) -> bool:
    return dir1[0] * dir2[0] + dir1[1] * dir2[1] == 0


def find_lowest_score(grid: Grid) -> int:
    start, target = find_start_and_target(grid)
    visited = set()
    nodes = [(0, (start, EAST))]
    while nodes:
        score, current = heappop(nodes)
        if current[0] == target:
            return score
        if current in visited:
            continue
        visited.add(current)

        for x, y in enumerate_free_neighbours(grid, current[0]):
            direction = calc_direction(source=current[0], target=(x, y))
            if direction == current[1]:
                new_node = ((x, y), direction)
                heappush(nodes, (score + 1, new_node))
            elif is_perpendicular(current[1], direction):
                new_node = (current[0], direction)
                heappush(nodes, (score + 1000, new_node))
    raise RuntimeError('Target not reachable')


Node = tuple[Point, Direction]
ScoredNodes = tuple[int, list[Node]]


def update_scores_bookkeeping(scores: dict[Node, ScoredNodes],
                              node: Node,
                              prev: Node,
                              distance: int) -> None:
    current_score, nodes = scores[node]
    if current_score == distance:
        nodes.append(prev)


def traverse_dijkstra(grid: Grid) -> tuple[Point, dict[Node, ScoredNodes]]:
    start, target = find_start_and_target(grid)
    visited = {}
    nodes =[(0, (start, EAST), None)]
    min_score = None
    while nodes:
        score, current, prev = heappop(nodes)
        if min_score is not None and score > min_score:
            break
        if current in visited:
            update_scores_bookkeeping(visited, current, prev, score)
            continue
        visited[current] = (score, [prev] if prev is not None else [])

        if current[0] == target:
            min_score = score
            continue

        for x, y in enumerate_free_neighbours(grid, current[0]):
            direction = calc_direction(source=current[0], target=(x, y))
            if direction == current[1]:
                new_node = ((x, y), direction)
                heappush(nodes, (score + 1, new_node, current))
            elif is_perpendicular(current[1], direction):
                new_node = (current[0], direction)
                heappush(nodes, (score + 1000, new_node, current))
    return target, visited


def extract_paths(node: Node, traversal_data: dict[Node, ScoredNodes]) -> list[list[Node]]:
    if node not in traversal_data:
        return []
    _, parents = traversal_data[node]
    if not parents:
        return [[node]]

    paths = list(itertools.chain.from_iterable(extract_paths(parent, traversal_data)
                                               for parent in parents))
    for path in paths:
        path.append(node)
    return paths


def extract_shortest_paths(target: Point,
                           traversal_data: dict[Node, ScoredNodes]) -> list[list[Node]]:
    result = []
    for direction in (EAST, WEST, NORTH, SOUTH):
        result.append(extract_paths((target, direction), traversal_data))
    return list(itertools.chain.from_iterable(result))


def count_tiles_on_shortest_path(grid: Grid) -> int:
    target, traversal = traverse_dijkstra(grid)
    paths = extract_shortest_paths(target, traversal)
    tiles = {point for point, _ in itertools.chain.from_iterable(paths)}
    return len(tiles)


def resolve_part1(input):
    return find_lowest_score(input)

def resolve_part2(input):
    return count_tiles_on_shortest_path(input)
