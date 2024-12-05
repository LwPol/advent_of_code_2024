import re
import itertools

XMAS_REGEX = re.compile('XMAS|SAMX')


def count_xmas_occurrences(text: str) -> int:
    result = 0
    idx = 0
    while (m := XMAS_REGEX.search(text, idx)) is not None:
        result += 1
        idx = m.start() + 1
    return result


def count_horizontal_occurrences(lines: list[str]) -> int:
    return sum(map(count_xmas_occurrences, lines))


def count_vertical_occurrences(lines: list[str]) -> int:
    width = len(lines[0])
    columns = (''.join(line[i] for line in lines) for i in range(width))
    return sum(map(count_xmas_occurrences, columns))


def get_dimensions(lines: list[str]) -> tuple[int, int]:
    return len(lines[0]), len(lines)


def north_west_diagonal(starting_point: tuple[int, int], lines: list[str]) -> str:
    width, height = get_dimensions(lines)
    point = starting_point
    result = ''
    while point[0] < width and point[1] < height:
        x, y = point
        result += lines[y][x]
        point = (x + 1, y + 1)
    return result


def count_north_west_diagonal_occurrences(lines: list[str]) -> int:
    width, height = get_dimensions(lines)
    points = itertools.chain(
        ((x, 0) for x in range(width)),
        ((0, y) for y in range(1, height))
    )
    return sum(count_xmas_occurrences(north_west_diagonal(p, lines)) for p in points)


def north_east_diagonal(starting_point: tuple[int, int], lines: list[str]) -> str:
    width, height = get_dimensions(lines)
    point = starting_point
    result = ''
    while point[0] >= 0 and point[1] < height:
        x, y = point
        result += lines[y][x]
        point = (x - 1, y + 1)
    return result


def count_north_east_diagonal_occurrences(lines: list[str]) -> int:
    width, height = get_dimensions(lines)
    points = itertools.chain(
        ((x, 0) for x in range(width)),
        ((width - 1, y) for y in range(1, height))
    )
    return sum(count_xmas_occurrences(north_east_diagonal(p, lines)) for p in points)


def count_all_occurrences(lines: list[str]) -> int:
    return (
        count_horizontal_occurrences(lines) +
        count_vertical_occurrences(lines) +
        count_north_west_diagonal_occurrences(lines) +
        count_north_east_diagonal_occurrences(lines)
    )


def is_center_of_x_mas(lines: list[str], point: tuple[int, int]) -> bool:
    x, y = point
    return (
        lines[y][x] == 'A' and
        {lines[y - 1][x - 1], lines[y + 1][x + 1]} == {'M', 'S'} and
        {lines[y - 1][x + 1], lines[y + 1][x - 1]} == {'M', 'S'}
    )


def count_all_x_mas_occurrences(lines: list[str]) -> int:
    width, height = get_dimensions(lines)
    points = itertools.product(range(1, width - 1), range(1, height - 1))
    return sum(1 for point in points if is_center_of_x_mas(lines, point))


def resolve_part1(input):
    return count_all_occurrences(input)

def resolve_part2(input):
    return count_all_x_mas_occurrences(input)