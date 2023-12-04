#!/bin/env python

from collections import defaultdict
import itertools
import re


class Schematic:
    def __init__(self, file_name: str):
        self._schematic: list[str] = []
        with open(file_name) as input_file:
            self._schematic: list[str] = [line.strip() for line in input_file]
        self.length = len(self._schematic)
        self.width = len(self._schematic[0])

    @staticmethod
    def _find_star_symbol(string: str) -> int | None:
        for x in range(len(string)):
            if string[x] == "*":
                return x
        return None

    def _find_gears(self) -> list[list[int]]:
        gear_adjacencies: dict[tuple[int, int], list[int]] = defaultdict(list)
        for x in range(self.length):
            line = self._schematic[x]
            for match in re.finditer(r"\d+", line):
                part_number = int(match.group())
                search_range = (
                    max(0, match.start() - 1),
                    min(self.width, match.end() + 1),
                )
                if (
                    x > 0
                    and (
                        location := self._find_star_symbol(
                            self._schematic[x - 1][search_range[0] : search_range[1]]
                        )
                    )
                    is not None
                ):
                    gear_adjacencies[(x - 1, search_range[0] + location)].append(
                        part_number
                    )
                if (
                    x < (self.length - 1)
                    and (
                        location := self._find_star_symbol(
                            self._schematic[x + 1][search_range[0] : search_range[1]]
                        )
                    )
                    is not None
                ):
                    gear_adjacencies[(x + 1, search_range[0] + location)].append(
                        part_number
                    )
                if (
                    match.start() > 0
                    and self._find_star_symbol(line[search_range[0]]) is not None
                ):
                    gear_adjacencies[(x, search_range[0])].append(part_number)
                if (
                    match.end() < (self.width - 1)
                    and self._find_star_symbol(line[search_range[1] - 1]) is not None
                ):
                    gear_adjacencies[(x, search_range[1] - 1)].append(part_number)
        return list(filter(lambda parts: len(parts) == 2, gear_adjacencies.values()))

    def sum_gear_ratios(self) -> int:
        gears = self._find_gears()
        return sum([gear[0] * gear[1] for gear in gears])


if __name__ == "__main__":
    print(Schematic("./simple_input.txt").sum_gear_ratios())
    print(Schematic("./input.txt").sum_gear_ratios())
