from collections import Counter


def parse_input_lists(lines: list[str]) -> tuple[list[int], list[int]]:
    left_list = []
    right_list = []
    for line in lines:
        tokens = line.split()
        left_list.append(int(tokens[0]))
        right_list.append(int(tokens[1]))
    return left_list, right_list


def calculate_total_distance(list1: list[int], list2: list[int]) -> int:
    return sum(abs(x - y) for x, y in zip(sorted(list1), sorted(list2)))


def calculate_similarity_score(left_list: list[int], right_list: list[int]) -> int:
    c = Counter(right_list)
    return sum(num * c[num] for num in left_list)


def resolve_part1(input):
    l1, l2 = parse_input_lists(input)
    return calculate_total_distance(l1, l2)

def resolve_part2(input):
    l1, l2 = parse_input_lists(input)
    return calculate_similarity_score(l1, l2)