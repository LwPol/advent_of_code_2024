import itertools
from typing import NamedTuple

Coords = tuple[int, int]
Direction = tuple[int, int]

class MapData(NamedTuple):
    width: int
    height: int
    obstructions: set[Coords]
    guard: Coords


class GuardsPositions(NamedTuple):
    visited_with_directions: set[tuple[Coords, Direction]]
    is_looped: bool


def process_map(lines: list[str]) -> set[Coords]:
    result = MapData(len(lines[0]), len(lines), set(), (0, 0))
    for x, y in itertools.product(range(result.width), range(result.height)):
        c = lines[y][x]
        if c == '#':
            result.obstructions.add((x, y))
        elif c == '^':
            result = result._replace(guard=(x, y))
    return result


def is_position_on_map(position: Coords, grid_size: tuple[int, int]) -> bool:
    width, height = grid_size
    x, y = position
    return x >= 0 and x < width and y >= 0 and y < height


def rotate_90_degrees(dx: int, dy: int) -> tuple[int, int]:
    if dx == 0:
        return (1, 0) if dy < 0 else (-1, 0)
    return (0, 1) if dx > 0 else (0, -1)


def track_guards_route(map_data: MapData) -> GuardsPositions:
    guard_pos = map_data.guard
    visited = set()
    dx = 0
    dy = -1
    while is_position_on_map(guard_pos, (map_data.width, map_data.height)):
        entry = (guard_pos, (dx, dy))
        if entry in visited:
            return GuardsPositions(visited, is_looped=True)
        visited.add((guard_pos, (dx, dy)))
        new_pos_candidate = (guard_pos[0] + dx, guard_pos[1] + dy)
        if new_pos_candidate in map_data.obstructions:
            dx, dy = rotate_90_degrees(dx, dy)
        else:
            guard_pos = new_pos_candidate
    return GuardsPositions(visited, is_looped=False)


def collect_visited_positions(map_data: MapData) -> set[Coords]:
    route = track_guards_route(map_data).visited_with_directions
    return {pos for pos, direction in route}


def check_if_putting_obstruction_loops_guard(map_data: MapData, coords: Coords) -> bool:
    map_data.obstructions.add(coords)
    result = track_guards_route(map_data).is_looped
    map_data.obstructions.remove(coords)
    return result


def count_looping_positions(map_data: MapData) -> int:
    visited = collect_visited_positions(map_data)
    visited.remove(map_data.guard)
    return sum(1 for pos in visited if check_if_putting_obstruction_loops_guard(map_data, pos))


def resolve_part1(input):
    return len(collect_visited_positions(process_map(input)))

def resolve_part2(input):
    return count_looping_positions(process_map(input))