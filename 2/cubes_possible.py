#!/bin/env python

import re

max_cubes: dict[str, int] = {"red": 12, "green": 13, "blue": 14}


def validate_game(line: str) -> int:
    game_breakdown = re.search(r"^Game (\d+):([\w,; ]*)$", line)
    game_number = int(game_breakdown.group(1))
    game_data = game_breakdown.group(2)
    for handful in re.split(";", game_data):
        for cube_data in re.split(",", handful):
            cube_data_breakdown = re.search(r" (\d+) (\w+)", cube_data)
            cube_count = int(cube_data_breakdown.group(1))
            cube_color = cube_data_breakdown.group(2)
            if cube_count > max_cubes[cube_color]:
                return 0
    return game_number


def check_cubes():
    with open("./input.txt") as input_file:
        print(sum(validate_game(line) for line in input_file.readlines()))


if __name__ == "__main__":
    check_cubes()
