#!/bin/env python

from typing import Callable
import operator

number_strings = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
}


def find_number(find_method: Callable, direction_operator: operator) -> str:
    best_location = -1
    best_value = "0"
    for search_string, value in number_strings.items():
        location = find_method(search_string)
        if location >= 0 and (
            direction_operator(location, best_location) or best_location < 0
        ):
            best_location = location
            best_value = value
    return best_value


def run_trebuchet() -> None:
    with open("./input.txt") as input_file:
        print(
            sum(
                int(
                    f"{find_number(line.find, operator.lt)}{find_number(line.rfind, operator.gt)}"
                )
                for line in input_file.readlines()
            )
        )


if __name__ == "__main__":
    run_trebuchet()
