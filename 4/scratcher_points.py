#!/bin/env python

import math


class Scratchers:
    def __init__(self, file_name: str):
        with open(file_name) as input_file:
            self._cards: list[str] = [line.strip() for line in input_file]

    @staticmethod
    def _tally_card(card: str) -> int:
        winning_section, numbers_section = card.split(":")[1].split("|")
        winning_values = [int(value) for value in winning_section.split()]
        number_values = [int(value) for value in numbers_section.split()]
        return math.floor(
            2
            ** (len([value for value in number_values if value in winning_values]) - 1)
        )

    def sum_winners(self) -> int:
        return sum([self._tally_card(card) for card in self._cards])


if __name__ == "__main__":
    print(Scratchers("./simple_input.txt").sum_winners())
    print(Scratchers("./input.txt").sum_winners())
