import itertools
from collections import OrderedDict


class DiskMapper:
    def __init__(self, disk_map: str):
        self._blocks = []
        self._free_space = OrderedDict()
        self._org_files_mapping = []
        self.__initialize(disk_map)

    def __initialize(self, disk_map: str):
        for idx, c in enumerate(disk_map):
            size = ord(c) - ord('0')
            next_block = len(self._blocks)
            if idx % 2 == 0:
                self._blocks.extend(itertools.repeat(idx // 2, size))
                self._org_files_mapping.append((next_block, size))
            else:
                self._blocks.extend(itertools.repeat(-1, size))
                self._free_space[next_block] = size

    def pack_blocks(self):
        last_free_idx = 0
        for block_idx, size in reversed(self._org_files_mapping):
            last_free_idx = self.__move_block_into_free_space(last_free_idx, block_idx, size)
            if last_free_idx == -1:
                break

    def pack_files(self):
        for block_idx, size in reversed(self._org_files_mapping):
            if self.__put_file_in_first_free_space(block_idx, size):
                for i in range(block_idx, block_idx + size):
                    self._blocks[i] = -1

    def checksum(self) -> int:
        return sum(idx * file_id for idx, file_id in enumerate(self._blocks) if file_id != -1)

    def __put_file_in_first_free_space(self,
                                       block_idx: int,
                                       block_size: int) -> bool:
        for idx, size in self._free_space.items():
            if idx > block_idx:
                break

            if size >= block_size:
                free_idx = self.__find_next_free_space(idx)
                for i in range(free_idx, free_idx + block_size):
                    self._blocks[i] = self._blocks[block_idx]
                if size == block_size:
                    del self._free_space[idx]
                else:
                    self._free_space[idx] -= block_size
                return True
        return False

    def __move_block_into_free_space(self,
                                     start_from: int,
                                     block_idx: int,
                                     block_size: int) -> int:
        for idx in range(block_idx + block_size - 1, block_idx - 1, -1):
            free_index = self.__find_next_free_space(start_from)
            if free_index >= block_idx:
                return -1
            self._blocks[free_index] = self._blocks[idx]
            self._blocks[idx] = -1
        return free_index

    def __find_next_free_space(self, start_from: int) -> int:
        return next(filter(lambda i: self._blocks[i] == -1, itertools.count(start_from)))


def resolve_part1(input):
    mapper = DiskMapper(input[0])
    mapper.pack_blocks()
    return mapper.checksum()

def resolve_part2(input):
    mapper = DiskMapper(input[0])
    mapper.pack_files()
    return mapper.checksum()
