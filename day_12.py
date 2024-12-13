from typing import NamedTuple, Optional, Callable
import itertools


Point = tuple[int, int]

class Region(NamedTuple):
    plots: set[Point]
    edges: set[tuple[Point, Point]]

PricingFunc = Callable[[Region], int]


def is_point_on_map(grid: list[str], point: Point) -> bool:
    x, y = point
    return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)


def get_plant(grid: list[str], point: Point) -> Optional[str]:
    x, y = point
    return grid[y][x] if is_point_on_map(grid, point) else None


def get_edge_between_tiles(inside: Point, outside: Point) -> tuple[Point, Point]:
    if inside[0] == outside[0]:
        y = inside[1] if inside[1] > outside[1] else outside[1]
        return ((inside[0], y), (inside[0] + 1, y))
    else:
        x = inside[0] if inside[0] > outside[0] else outside[0]
        return ((x, inside[1]), (x, inside[1] + 1))


def map_out_impl(grid: list[str],
                 current: Point,
                 plots: set[Point],
                 edges: set[tuple[Point, Point]]) -> list[Point]:
    plant = get_plant(grid, current)
    dxs = (1, 0, -1, 0)
    dys = (0, 1, 0, -1)
    points_for_visit = []
    for dx, dy in zip(dxs, dys):
        neighbour = (current[0] + dx, current[1] + dy)
        next_plant = get_plant(grid, neighbour)
        if next_plant != plant:
            edges.add(get_edge_between_tiles(inside=current, outside=neighbour))
        elif neighbour not in plots:
            points_for_visit.append(neighbour)
    return points_for_visit


def flood_region(grid: list[str],
                 generation: set[Point],
                 plots: set[Point],
                 edges: set[tuple[Point, Point]]):
    next_generation = set()
    for tile in generation:
        next_generation.update(map_out_impl(grid, tile, plots, edges))

    if next_generation:
        plots.update(next_generation)
        flood_region(grid, next_generation, plots, edges)    


def map_out_region(grid: list[str], starting_plot: Point) -> Region:
    result = Region(plots={starting_plot}, edges=set())
    flood_region(grid, {starting_plot}, result.plots, result.edges)
    return result


def find_all_regions(grid: list[str]) -> list[Region]:
    result = []
    unmapped = set(itertools.product(range(len(grid[0])), range(len(grid))))
    while unmapped:
        result.append(map_out_region(grid, next(iter(unmapped))))
        unmapped -= result[-1].plots
    return result


def get_total_price(region: Region) -> int:
    area = len(region.plots)
    perimeter = len(region.edges)
    return area * perimeter


def estimate_fence_cost(grid: list[str], pricing_method: PricingFunc) -> int:
    regions = find_all_regions(grid)
    return sum(map(pricing_method, regions))


def move_along_y_axis(edge: tuple[Point, Point], dy: int):
    while True:
        p1, p2 = edge
        edge = ((p1[0], p1[1] + dy), (p2[0], p2[1] + dy))
        yield edge


def move_along_x_axis(edge: tuple[Point, Point], dx: int):
    while True:
        p1, p2 = edge
        edge = ((p1[0] + dx, p1[1]), (p2[0] + dx, p2[1]))
        yield edge


def check_cross_cornercase(edges: set[tuple[Point, Point]],
                           edge: tuple[Point, Point],
                           direction: Point) -> bool:
    dx, dy = direction
    p1, p2 = edge
    if dx == 0:
        y = p2[1] if dy < 0 else p1[1]
        x = p1[0]
        return ((x - 1, y), (x, y)) not in edges and ((x, y), (x + 1, y)) not in edges
    x = p2[0] if dx < 0 else p1[0]
    y = p1[1]
    return ((x, y - 1), (x, y)) not in edges and ((x, y), (x, y + 1)) not in edges


def reduce_edge_to_side(starting_edge: tuple[Point, Point],
                        edges: set[tuple[Point, Point]]) -> set[tuple[Point, Point]]:
    def belongs_to_side(direction: tuple[Point, Point]) -> Callable[[tuple[Point, Point]], bool]:
        return lambda edge: edge in edges and check_cross_cornercase(edges, edge, direction)
    p1, p2 = starting_edge
    side = {starting_edge}
    if p1[0] == p2[0]:
        side.update(itertools.takewhile(belongs_to_side((0, -1)), move_along_y_axis(starting_edge, -1)))
        side.update(itertools.takewhile(belongs_to_side((0, 1)), move_along_y_axis(starting_edge, 1)))
    else:
        side.update(itertools.takewhile(belongs_to_side((-1, 0)), move_along_x_axis(starting_edge, -1)))
        side.update(itertools.takewhile(belongs_to_side((1, 0)), move_along_x_axis(starting_edge, 1)))
    return side


def count_sides(edges: set[tuple[Point, Point]]) -> int:
    sides = 0
    copy = set(edges)
    while copy:
        extracted_side = reduce_edge_to_side(next(iter(copy)), edges)
        copy -= extracted_side
        sides += 1
    return sides


def get_discounted_price(region: Region) -> int:
    area = len(region.plots)
    sides = count_sides(region.edges)
    return area * sides


def resolve_part1(input):
    return estimate_fence_cost(input, get_total_price)

def resolve_part2(input):
    return estimate_fence_cost(input, get_discounted_price)
