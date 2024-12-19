def parse_input(lines: list[str]) -> tuple[list[str], list[str]]:
    return lines[0].split(', '), lines[2:]


class CachedTowelsArrangement:
    def __init__(self, patterns: list[str]):
        self._patterns = patterns
        self._cache = {}
        self._counts_cache = {}

    def is_pattern_possible(self, design: str) -> bool:
        if not design:
            return True

        if design in self._cache:
            return self._cache[design]

        ret = self.__is_pattern_possible_impl(design)
        self._cache[design] = ret
        return ret

    def __is_pattern_possible_impl(self, design: str) -> bool:
        for pattern in self._patterns:
            if (design.startswith(pattern)
                and self.is_pattern_possible(design[len(pattern):])):
                return True
        return False

    def count_arrangements(self, design: str) -> int:
        if not design:
            return 1

        if design in self._counts_cache:
            return self._counts_cache[design]
        
        ret = self.__count_arrangements_impl(design)
        self._counts_cache[design] = ret
        return ret

    def __count_arrangements_impl(self, design: str) -> int:
        result = 0
        for pattern in self._patterns:
            if design.startswith(pattern):
                result += self.count_arrangements(design[len(pattern):])
        return result


def count_possible_patterns(patterns: list[str], designs: list[str]) -> int:
    obj = CachedTowelsArrangement(patterns)
    return sum(1 for design in designs if obj.is_pattern_possible(design))


def count_all_arrangements(patterns: list[str], designs: list[str]) -> int:
    obj = CachedTowelsArrangement(patterns)
    return sum(obj.count_arrangements(design) for design in designs)


def resolve_part1(input):
    return count_possible_patterns(*parse_input(input))

def resolve_part2(input):
    return count_all_arrangements(*parse_input(input))
