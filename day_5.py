from collections import defaultdict


Rule = tuple[int, int]
Update = list[int]


def parse_rules(lines: list[str]) -> list[Rule]:
    def parse_one(text: str) -> Rule:
        lhs, rhs = text.split('|')
        return int(lhs), int(rhs)
    return [parse_one(line) for line in lines]


def parse_updates(lines: list[str]) -> list[Update]:
    return [[int(num) for num in line.split(',')] for line in lines]


def parse_input(lines: list[str]) -> tuple[list[Rule], list[Update]]:
    split_idx = lines.index('')
    return parse_rules(lines[:split_idx]), parse_updates(lines[split_idx + 1:])


def create_priorities_map(rules: list[Rule]) -> dict[int, set[int]]:
    result = defaultdict(set)
    for lhs, rhs in rules:
        result[lhs].add(rhs)
    return result


def is_correct_update(update: Update, rules_map: dict[int, set[int]]) -> bool:
    processed_pages = set()
    for page in update:
        if processed_pages.intersection(rules_map[page]):
            return False
        processed_pages.add(page)
    return True


def sum_middle_pages_for_correct_updates(updates: list[Update], rules: list[Rule]) -> int:
    priorities = create_priorities_map(rules)
    return sum(update[len(update) // 2] for update in updates
               if is_correct_update(update, priorities))


def find_insertion_index(update: Update, look_for: set[int]) -> int:
    it = filter(lambda elem: elem[1] in look_for, enumerate(update))
    return next(it)[0]


def fix_update(update: list[Update], rules_map: dict[int, set[int]]) -> Update:
    fixed = update[:]
    pages = set()
    idx = 0
    while idx < len(update):
        page = fixed[idx]
        if (common := pages.intersection(rules_map[page])):
            fixed = fixed[:idx] + fixed[idx + 1:]
            new_idx = find_insertion_index(fixed, common)
            fixed.insert(new_idx, page)
            idx = new_idx + 1
            pages = set(fixed[:idx])
        else:
            pages.add(page)
            idx += 1
    return fixed


def sum_middle_pages_for_fixed_updates(updates: list[Update], rules: list[Rule]) -> int:
    priorities = create_priorities_map(rules)
    fixed_updates = (fix_update(update, priorities) for update in updates
                     if not is_correct_update(update, priorities))
    return sum(item[len(item) // 2] for item in fixed_updates)


def resolve_part1(input):
    rules, updates = parse_input(input)
    return sum_middle_pages_for_correct_updates(updates, rules)

def resolve_part2(input):
    rules, updates = parse_input(input)
    return sum_middle_pages_for_fixed_updates(updates, rules)
