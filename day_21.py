import itertools
from typing import Optional


Point = tuple[int, int]
KeypadDistanceMapping = dict[Point, int]


NUMERIC_KEYPAD = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '0': (1, 3),
    'A': (2, 3),
    'blank': (0, 3),
}

DIRECTIONAL_KEYPAD = {
    '<': (0, 1),
    '^': (1, 0),
    'v': (1, 1),
    'A': (2, 0),
    '>': (2, 1),
    'blank': (0, 0),
}


def move_in_straight_line(source: Point, target: Point) -> str:
    if source[0] == target[0]:
        key = '^' if target[1] < source[1] else 'v'
        return ''.join(itertools.repeat(key, abs(source[1] - target[1])))
    key = '<' if target[0] < source[0] else '>'
    return ''.join(itertools.repeat(key, abs(source[0] - target[0])))


def move_diagonally_beginning_with_direction(keypad: dict[str, Point],
                                             source: Point,
                                             target: Point,
                                             starting_dir: str) -> Optional[str]:
    if starting_dir == '>' or starting_dir == '<':
        mid = (target[0], source[1])
        if mid == keypad['blank']:
            return None
    else:
        mid = (source[0], target[1])
        if mid == keypad['blank']:
            return None
    return move_in_straight_line(source, mid) + move_in_straight_line(mid, target)


def get_direction_keys(dx: int, dy: int) -> tuple[str, str]:
    xx = '>' if dx > 0 else '<'
    yy = '^' if dy < 0 else 'v'
    return (xx, yy)


def find_paths_for_button_click(keypad: dict[str, Point], start: str, end: str) -> list[str]:
    source = keypad[start]
    target = keypad[end]
    dx = target[0] - source[0]
    dy = target[1] - source[1]
    if dx == 0 or dy == 0:
        return [move_in_straight_line(source, target) + 'A']

    d1, d2 = get_direction_keys(dx, dy)
    opt1 = move_diagonally_beginning_with_direction(keypad, source, target, d1)
    opt2 = move_diagonally_beginning_with_direction(keypad, source, target, d2)
    result = [opt + 'A' for opt in (opt1, opt2) if opt is not None]

    if not result:
        raise RuntimeError('Failed to find path')
    return result



def enumerate_button_pairs(keypad: dict[str, Point]):
    return filter(lambda p: p[0] != 'blank' and p[1] != 'blank',
                  itertools.product(keypad.keys(), repeat=2))


def map_distances_between_keys(prev_keypad: KeypadDistanceMapping,
                               keypad: dict[str, Point]) -> KeypadDistanceMapping:
    def calculate_clicks_for_keypad_path(path: str) -> int:
        return sum(prev_keypad[pair] for pair in itertools.pairwise('A' + path))
    result = {}
    for key_from, key_to in enumerate_button_pairs(keypad):
        paths = find_paths_for_button_click(keypad, key_from, key_to)
        result[(key_from, key_to)] = min(map(calculate_clicks_for_keypad_path, paths))
    return result


def make_numeric_keypad_clicks_map(intermediates: int) -> KeypadDistanceMapping:
    temp = {pair: 1 for pair in enumerate_button_pairs(DIRECTIONAL_KEYPAD)}
    for _ in range(intermediates):
        temp = map_distances_between_keys(temp, DIRECTIONAL_KEYPAD)
    return map_distances_between_keys(temp, NUMERIC_KEYPAD)


def get_fewest_clicks_for_code(mapping: KeypadDistanceMapping, code: str) -> int:
    return sum(mapping[pair] for pair in itertools.pairwise('A' + code))


def calculate_complexity(mapping: KeypadDistanceMapping, code: str) -> int:
    return get_fewest_clicks_for_code(mapping, code) * int(code[:-1])


def sum_complexities(codes: list[str], intermediates: int = 2) -> int:
    mapping = make_numeric_keypad_clicks_map(intermediates)
    return sum(calculate_complexity(mapping, code) for code in codes)


def resolve_part1(input):
    return sum_complexities(input)

def resolve_part2(input):
    return sum_complexities(input, intermediates=25)
