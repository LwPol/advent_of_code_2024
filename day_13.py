from typing import NamedTuple, Optional
import re


class ClawMachineConfig(NamedTuple):
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]


BUTTON_REGEX = re.compile(r'Button (A|B): X\+(\d+), Y\+(\d+)')
PRIZE_REGEX = re.compile(r'Prize: X=(\d+), Y=(\d+)')


def parse_configuration(lines: list[str]) -> ClawMachineConfig:
    button_type, xa, ya = BUTTON_REGEX.match(lines[0]).groups()
    if button_type != 'A':
        raise RuntimeError('Bad input')
    _, xb, yb = BUTTON_REGEX.match(lines[1]).groups()
    prize_x, prize_y = PRIZE_REGEX.match(lines[2]).groups()
    return ClawMachineConfig(
        button_a=(int(xa), int(ya)),
        button_b=(int(xb), int(yb)),
        prize=(int(prize_x), int(prize_y))
    )


def parse_input(lines: list[str]) -> list[ClawMachineConfig]:
    return [parse_configuration(lines[i:i + 4]) for i in range(0, len(lines), 4)]


def get_determinant(matrix: list[list[int]]) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def solve_config_in_real_domain(config: ClawMachineConfig) -> tuple[float, float]:
    xa, ya = config.button_a
    xb, yb = config.button_b
    px, py = config.prize

    main_det = get_determinant([[xa, xb], [ya, yb]])
    # all of input configs seem to have non-zero determinant
    n1 = get_determinant([[px, xb], [py, yb]]) / main_det
    n2 = get_determinant([[xa, px], [ya, py]]) / main_det
    return n1, n2


def check_solution(config: ClawMachineConfig, a_pushes: int, b_pushes: int) -> bool:
    xa, ya = config.button_a
    xb, yb = config.button_b
    px, py = config.prize
    return a_pushes * xa + b_pushes * xb == px and a_pushes * ya + b_pushes * yb == py


def solve_config(config: ClawMachineConfig) -> Optional[tuple[int, int]]:
    n1, n2 = solve_config_in_real_domain(config)
    a_pushes = round(n1)
    b_pushes = round(n2)
    return (a_pushes, b_pushes) if check_solution(config, a_pushes, b_pushes) else None


def count_tokens_for_wins(machines: list[ClawMachineConfig]) -> int:
    def get_tokens_to_win(pushes: tuple[int, int]) -> int:
        a, b = pushes
        return 3 * a + b
    solutions = map(solve_config, machines)
    return sum(get_tokens_to_win(elem) for elem in solutions if elem is not None)


def account_for_conversion_error(configs: list[ClawMachineConfig]) -> list[ClawMachineConfig]:
    error = 10000000000000
    return [ClawMachineConfig(c.button_a, c.button_b,
                              prize=(error + c.prize[0], error + c.prize[1]))
            for c in configs]


def resolve_part1(input):
    return count_tokens_for_wins(parse_input(input))

def resolve_part2(input):
    return count_tokens_for_wins(account_for_conversion_error(parse_input(input)))
