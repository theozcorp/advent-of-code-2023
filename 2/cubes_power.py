#!/bin/env python

import math
import re


def calculate_cube_power(line: str) -> int:
    min_cubes: dict[str, int] = {"red": 0, "green": 0, "blue": 0}
    game_breakdown = re.search(r"^Game (\d+):([\w,; ]*)$", line)
    game_data = game_breakdown.group(2)
    for handful in re.split(";", game_data):
        for cube_data in re.split(",", handful):
            cube_data_breakdown = re.search(r" (\d+) (\w+)", cube_data)
            cube_count = int(cube_data_breakdown.group(1))
            cube_color = cube_data_breakdown.group(2)
            min_cubes[cube_color] = max(cube_count, min_cubes[cube_color])
    return math.prod(min_cubes.values())


def check_cubes():
    with open("./input.txt") as input_file:
        print(sum(calculate_cube_power(line) for line in input_file.readlines()))


if __name__ == "__main__":
    check_cubes()
