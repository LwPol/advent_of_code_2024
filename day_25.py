from collections import defaultdict
import itertools

KeysBuckets = dict[int, list[str]]
LocksBuckets = dict[int, list[str]]
Key = list[int]
Lock = list[int]


def is_lock(item: list[str]) -> bool:
    return item[0][0] == '#'


def item_to_column_heights(item: list[str]) -> list[int]:
    return [sum(1 for j in range(1, 6) if item[j][i] == '#') for i in range(5)]


def count_internal_hashes(item: list[str]) -> int:
    return sum(1 for x, y in itertools.product(range(5), range(1, 6))
               if item[y][x] == '#')


def parse_locks_and_keys(lines: list[str]) -> tuple[list[Lock], list[Key]]:
    locks = []
    keys = []
    idx = 0
    while idx < len(lines):
        next_idx = next((i for i in range(idx, len(lines)) if lines[i] == ''), None)
        if next_idx is None:
            next_idx = len(lines)

        item = lines[idx:next_idx]
        if is_lock(item):
            locks.append(item_to_column_heights(item))
        else:
            keys.append(item_to_column_heights(item))
        idx = next_idx + 1
    return locks, keys


def count_overlapping_keys(lock: Lock, keys: list[Key]) -> bool:
    return sum(1 for key in keys if all(lock[i] + key[i] <= 5 for i in range(5)))


def count_fitting_lock_key_pairs(locks: list[Lock], keys: list[Key]) -> int:
    return sum(count_overlapping_keys(lock, keys) for lock in locks)


def resolve_part1(input):
    return count_fitting_lock_key_pairs(*parse_locks_and_keys(input))

def resolve_part2(input):
    return 'Merry Christmas'
