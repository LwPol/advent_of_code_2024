from collections import defaultdict
import itertools
from heapq import heapify, heappop, heappush

Connections = dict[str, set[str]]


class NodesWrapper:
    def __init__(self, for_check: set[str], network: set[str]):
        self.for_check = for_check
        self.network = network
    
    def __lt__(self, other):
        return len(self.network) + len(self.for_check) > len(other.network) + len(other.for_check)

    def __repr__(self):
        return f'{self.network}: {self.for_check}'


def parse_network(lines: list[str]) -> Connections:
    result = defaultdict(set)
    for line in lines:
        node1, node2 = line.split('-')
        result[node1].add(node2)
        result[node2].add(node1)
    return result


def count_computer_sets(connections: Connections) -> int:
    sets = set()
    for node, connected in filter(lambda n: n[0].startswith('t'), connections.items()):
        for n2, n3 in itertools.combinations(connected, r=2):
            if n2 in connections[n3]:
                sets.add(tuple(sorted((node, n2, n3))))
    return len(sets)


def init_interconnected_nodes_heap(connections: Connections) -> list[NodesWrapper]:
    def largest_set_for_pair(node1: str, node2: str) -> NodesWrapper:
        common = connections[node1] & connections[node2]
        return NodesWrapper(common, {node1, node2})
    pairs = filter(lambda p: p[0] in connections[p[1]],
                   itertools.combinations(connections.keys(), r=2))
    result = [largest_set_for_pair(*nodes) for nodes in pairs]
    heapify(result)
    return result


def find_largest_interconnected_set(connections: Connections) -> set[str]:
    queue = init_interconnected_nodes_heap(connections)
    while queue:
        wrapper = heappop(queue)
        if not wrapper.for_check:
            return wrapper.network

        for node in wrapper.for_check:
            if wrapper.network <= connections[node]:
                new_check = wrapper.for_check & connections[node]
                heappush(queue, NodesWrapper(new_check, wrapper.network | {node}))
    raise RuntimeError('Error occurred')


def resolve_part1(input):
    return count_computer_sets(parse_network(input))

def resolve_part2(input):
    lan_party = find_largest_interconnected_set(parse_network(input))
    return ','.join(sorted(lan_party))
