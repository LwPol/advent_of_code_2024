from collections import Counter


def parse_stones(line: str) -> list[int]:
    return [int(num) for num in line.split()]


def count_rocks(stones: list[int]) -> dict[int, int]:
    return Counter(stones)


def replace_rocks_after_blink(stones_coutner: dict[int, int]) -> dict[int, int]:
    result = Counter()
    for stone, count in stones_coutner.items():
        if stone == 0:
            result[1] += count
        else:
            as_str = str(stone)
            mid = len(as_str) // 2
            if len(as_str) % 2 == 0:
                result[int(as_str[:mid])] += count
                result[int(as_str[mid:])] += count
            else:
                result[2024 * stone] += count
    return result


def count_stones_after_blinking(stones: list[int], times: int) -> int:
    counter = count_rocks(stones)
    for _ in range(times):
        counter = replace_rocks_after_blink(counter)
    return sum(counter.values())


def resolve_part1(input):
    return count_stones_after_blinking(parse_stones(input[0]), times=25)

def resolve_part2(input):
    return count_stones_after_blinking(parse_stones(input[0]), times=75)
