import itertools

Point = tuple[int, int]


def iterate_over_trail_starts(topo_map: list[str]):
    def is_trail_start(point):
        x, y = point
        return topo_map[y][x] == '0'
    return filter(is_trail_start,
                  itertools.product(range(len(topo_map[0])), range(len(topo_map))))


def is_on_map(topo_map: list[str], point: Point) -> bool:
    x, y = point
    width = len(topo_map[0])
    height = len(topo_map)
    return x >= 0 and x < width and y >= 0 and y < height


def digit_to_int(digit: str) -> int:
    return ord(digit) - ord('0')


def get_height_at_point(topo_map: list[str], point: Point) -> int:
    x, y = point
    return digit_to_int(topo_map[y][x])


def traverse_trail(topo_map: list[str], current: Point, peeks: set[Point]):
    height = get_height_at_point(topo_map, current)
    if height == 9:
        peeks.add(current)
        return

    dxs = (1, 0, -1, 0)
    dys = (0, 1, 0, -1)
    for dx, dy in zip(dxs, dys):
        next_pt = (current[0] + dx, current[1] + dy)
        if is_on_map(topo_map, next_pt):
            new_height = get_height_at_point(topo_map, next_pt)
            if new_height - height == 1:
                traverse_trail(topo_map, next_pt, peeks)


def score_trail(topo_map: list[str], point: Point) -> int:
    peeks = set()
    traverse_trail(topo_map, point, peeks)
    return len(peeks)


def rate_trail(topo_map: list[str], point: Point) -> int:
    height = get_height_at_point(topo_map, point)
    if height == 9:
        return 1

    dxs = (1, 0, -1, 0)
    dys = (0, 1, 0, -1)
    rate = 0
    for dx, dy in zip(dxs, dys):
        next_pt = (point[0] + dx, point[1] + dy)
        if is_on_map(topo_map, next_pt):
            new_height = get_height_at_point(topo_map, next_pt)
            if new_height - height == 1:
                rate += rate_trail(topo_map, next_pt)
    return rate


def sum_trails_scores(topo_map: list[str]) -> int:
    return sum(score_trail(topo_map, point) for point in iterate_over_trail_starts(topo_map))


def sum_trails_rates(topo_map: list[str]) -> int:
    return sum(rate_trail(topo_map, point) for point in iterate_over_trail_starts(topo_map))


def resolve_part1(input):
    return sum_trails_scores(input)

def resolve_part2(input):
    return sum_trails_rates(input)
