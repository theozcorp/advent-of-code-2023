#!/bin/env python

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
    def _does_string_contain_symbol(string: str) -> bool:
        for char in string:
            if char != "." and not char.isnumeric():
                return True
        return False

    def sum_part_numbers(self) -> int:
        sum = 0
        for x in range(self.length):
            line = self._schematic[x]
            for match in re.finditer(r"\d+", line):
                if (
                    (
                        x > 0
                        and self._does_string_contain_symbol(
                            self._schematic[x - 1][
                                max(0, match.start() - 1) : min(
                                    self.width, match.end() + 1
                                )
                            ]
                        )
                    )
                    or (
                        x < (self.length - 1)
                        and self._does_string_contain_symbol(
                            self._schematic[x + 1][
                                max(0, match.start() - 1) : min(
                                    self.width, match.end() + 1
                                )
                            ]
                        )
                    )
                    or (
                        match.start() > 0
                        and self._does_string_contain_symbol(line[match.start() - 1])
                    )
                    or (
                        match.end() < (self.width - 1)
                        and self._does_string_contain_symbol(line[match.end()])
                    )
                ):
                    sum += int(match.group())
                    continue
        return sum


if __name__ == "__main__":
    print(Schematic("./simple_input.txt").sum_part_numbers())
    print(Schematic("./input.txt").sum_part_numbers())
