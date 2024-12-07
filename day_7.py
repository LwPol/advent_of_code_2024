from typing import Callable

Equation = tuple[int, list[int]]
Operator = Callable[[int, int], int]


def parse_equations(lines: list[str]) -> list[Equation]:
    def parse_line(line: str) -> Equation:
        tokens = line.split(':')
        test_value = int(tokens[0])
        numbers = [int(num) for num in tokens[1].split()]
        return test_value, numbers
    return list(map(parse_line, lines))


def check_combination(target_value: int,
                      current_value: int,
                      operators: list[Operator],
                      numbers: list[int]) -> bool:
    if not numbers:
        return current_value == target_value

    for op in operators:
        new_val = op(current_value, numbers[0])
        if new_val <= target_value and check_combination(target_value, new_val, operators, numbers[1:]):
            return True
    return False


def is_valid_equation(equation: Equation, operators: list[Operator]) -> bool:
    test_value, numbers = equation
    return check_combination(test_value, numbers[0], operators, numbers[1:])


def get_total_calibration_result(equations: list[Equation]) -> int:
    ops = [lambda x, y: x + y, lambda x, y: x * y]
    return sum(eq[0] for eq in equations if is_valid_equation(eq, ops))


def get_total_calibration_result_fixed(equations: list[Equation]) -> int:
    ops = [lambda x, y: x + y, lambda x, y: x * y, lambda x, y: int(str(x) + str(y))]
    return sum(eq[0] for eq in equations if is_valid_equation(eq, ops))


def resolve_part1(input):
    return get_total_calibration_result(parse_equations(input))

def resolve_part2(input):
    return get_total_calibration_result_fixed(parse_equations(input))