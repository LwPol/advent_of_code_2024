from collections import Counter
from typing import Iterable

Diff = tuple[int, int, int, int]


def derive_new_secret(current: int) -> int:
    current ^= 64 * current
    current %= 16777216
    current ^= current // 32
    current %= 16777216
    current ^= 2048 * current
    current %= 16777216
    return current


def calculate_secret(secret: int, sells: int) -> int:
    for _ in range(sells):
        secret = derive_new_secret(secret)
    return secret


def get_price(secret: int) -> int:
    return secret % 10


def generate_price_changes(secret: int, total_sells: int):
    diffs = []
    prices = []
    for _ in range(total_sells):
        new_secret = derive_new_secret(secret)
        current_price = get_price(new_secret)
        diffs.append(current_price - get_price(secret))
        prices.append(current_price)
        secret = new_secret
    return zip(diffs, diffs[1:], diffs[2:], diffs[3:], prices[3:])


def record_profits(profits: dict[Diff, int], init_secret: int, total_sells: int) -> None:
    recorded = set()
    for d1, d2, d3, d4, price in generate_price_changes(init_secret, total_sells):
        pattern = (d1, d2, d3, d4)
        if pattern not in recorded:
            profits[pattern] += price
            recorded.add(pattern)


def record_possible_profits(buyers: Iterable[int], sells: int) -> dict[Diff, int]:
    profits = Counter()
    for buyer in buyers:
        record_profits(profits, buyer, sells)
    return profits


def find_max_bananas(buyers: Iterable[int], sells: int) -> int:
    return max(record_possible_profits(buyers, sells).values())


def resolve_part1(input):
    return sum(calculate_secret(int(line), sells=2000) for line in input)

def resolve_part2(input):
    return find_max_bananas(map(int, input), sells=2000)
