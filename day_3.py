import re


MUL_PATTERN = r'mul\((\d{1,3}),(\d{1,3})\)'
ENABLE_PATTERN = r'do\(\)'
DISABLE_PATTERN = r"don't\(\)"


def generate_matches(text: str, pattern: str):
    regex = re.compile(pattern)
    idx = 0
    while (re_match := regex.search(text, idx)) is not None:
        idx = re_match.end()
        yield re_match


def execute_multiplications(memory: str) -> int:
    return sum(int(m.group(1)) * int(m.group(2)) for m in generate_matches(memory, MUL_PATTERN))


def execute_conditionally(memory: str) -> int:
    enabled = True
    inst_regex = re.compile('|'.join([MUL_PATTERN, ENABLE_PATTERN, DISABLE_PATTERN]))
    result = 0
    for match in generate_matches(memory, inst_regex):
        matched = match.group()
        if matched.startswith('mul'):
            if enabled:
                result += int(match.group(1)) * int(match.group(2))
        elif matched.startswith("don't"):
            enabled = False
        else:
            enabled = True
    return result


def resolve_part1(input):
    return execute_multiplications(''.join(input))

def resolve_part2(input):
    return execute_conditionally(''.join(input))
