import itertools


Grid = list[list[str]]
Moves = str
Point = tuple[int, int]


def parse_input(lines: list[str]) -> tuple[Grid, Moves]:
    splitIdx = next(filter(lambda elem: not elem[1], enumerate(lines)))[0]
    grid = [list(line) for line in lines[:splitIdx]]
    moves = ''.join(lines[splitIdx + 1:])
    return grid, moves


def get_grid_size(grid: Grid) -> tuple[int, int]:
    return len(grid[0]), len(grid)


def get_object_at(grid: Grid, point: Point) -> str:
    x, y = point
    return grid[y][x]


def find_robot_position(grid: Grid) -> Point:
    width, height = get_grid_size(grid)
    for pos in itertools.product(range(width), range(height)):
        if get_object_at(grid, pos) == '@':
            return pos
    raise RuntimeError('Robot not found')


def get_direction_from_move(move: str) -> tuple[int, int]:
    if move == '^':
        return (0, -1)
    if move == 'v':
        return (0, 1)
    if move == '>':
        return (1, 0)
    if move == '<':
        return (-1, 0)
    raise RuntimeError('Invalid move')


def get_next_position(current: Point, move: str) -> Point:
    x, y = current
    dx, dy = get_direction_from_move(move)
    return (x + dx, y + dy)


def move_object(grid: Grid, source: Point, target: Point) -> None:
    obj = get_object_at(grid, source)
    grid[target[1]][target[0]] = obj
    grid[source[1]][source[0]] = '.'


def try_moving_to_new_position(grid: Grid, current: Point, direction: Point) -> bool:
    x, y = current
    dx, dy = direction
    new_pos = (x + dx, y + dy)
    obj = get_object_at(grid, new_pos)
    if obj == '#':
        return False
    if obj == '.':
        move_object(grid, source=current, target=new_pos)
        return True

    if try_moving_to_new_position(grid, new_pos, direction):
        move_object(grid, source=current, target=new_pos)
        return True
    return False


def move_robot(grid: Grid, robot_position: Point, move: str) -> Point:
    dx, dy = get_direction_from_move(move)
    if try_moving_to_new_position(grid, robot_position, (dx, dy)):
        return robot_position[0] + dx, robot_position[1] + dy
    return robot_position


def perform_move_sequence(grid: Grid, moves: Moves) -> None:
    robot = find_robot_position(grid)
    for move in moves:
        robot = move_robot(grid, robot, move)


def sum_boxes_gps(grid: Grid, box: str = 'O') -> int:
    width, height = get_grid_size(grid)
    boxes = filter(lambda pt: get_object_at(grid, pt) == box,
                   itertools.product(range(width), range(height)))
    return sum(x + 100 * y for x, y in boxes)


def prepare_p2_layout(grid: Grid) -> Grid:
    transform = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.',
    }
    return [list(''.join(transform[c] for c in row)) for row in grid]


def is_move_possible(grid: Grid, current: Point, direction: Point) -> bool:
    x, y = current
    dx, dy = direction
    new_pos = (x + dx, y + dy)
    obj = get_object_at(grid, new_pos)
    
    if obj == '[' or obj == ']':
        if dy == 0:
            return is_move_possible(grid, (x + 2 * dx, y), direction)
        else:
            other_part = (new_pos[0] + (1 if obj == '[' else -1), new_pos[1])
            return (is_move_possible(grid, new_pos, direction) and
                    is_move_possible(grid, other_part, direction))
    else:
        return obj == '.'
    

def move_element_among_large_boxes(grid: Grid, current: Point, direction: Point) -> Point:
    x, y = current
    dx, dy = direction
    new_pos = (x + dx, y + dy)
    obj = get_object_at(grid, new_pos)
    if obj == '[' or obj == ']':
        large_box = new_pos if obj == '[' else (new_pos[0] - 1, new_pos[1])
        move_large_box(grid, large_box, direction)
    move_object(grid, source=current, target=new_pos)
    return new_pos


def large_box_second_part(box_position: Point) -> Point:
    x, y = box_position
    return (x + 1, y)


def move_large_box(grid: Grid, box_position: Point, direction: Point) -> None:
    dx, dy = direction
    if dy == 0 and dx < 0:
        move_element_among_large_boxes(grid, box_position, direction)
        move_element_among_large_boxes(grid, large_box_second_part(box_position), direction)
    elif dy == 0 and dx > 0:
        move_element_among_large_boxes(grid, large_box_second_part(box_position), direction)
        move_element_among_large_boxes(grid, box_position, direction)
    else:
        move_element_among_large_boxes(grid, box_position, direction)
        move_element_among_large_boxes(grid, large_box_second_part(box_position), direction)


def move_robot_among_large_boxes(grid: Grid, robot_position: Point, move: str) -> Point:
    direction = get_direction_from_move(move)
    if is_move_possible(grid, robot_position, direction):
        return move_element_among_large_boxes(grid, robot_position, direction)
    return robot_position


def perform_move_sequence_p2(grid: Grid, moves: str) -> None:
    robot = find_robot_position(grid)
    for move in moves:
        robot = move_robot_among_large_boxes(grid, robot, move)


def resolve_part1(input):
    grid, moves = parse_input(input)
    perform_move_sequence(grid, moves)
    return sum_boxes_gps(grid)

def resolve_part2(input):
    grid, moves = parse_input(input)
    snd_warehouse = prepare_p2_layout(grid)
    perform_move_sequence_p2(snd_warehouse, moves)
    return sum_boxes_gps(snd_warehouse, box='[')
