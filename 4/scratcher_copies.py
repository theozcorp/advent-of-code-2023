#!/bin/env python

import math


class Scratchers:
    def __init__(self, file_name: str):
        with open(file_name) as input_file:
            self._cards: list[str] = [line.strip() for line in input_file]
        self._card_counts: dict[int, int] = {i: 1 for i in range(len(self._cards))}
        self._card_winners_count: dict[int, int] = {
            i: 0 for i in range(len(self._cards))
        }

    def _tally_card(self, card_index: int) -> None:
        winning_section, numbers_section = (
            self._cards[card_index].split(":")[1].split("|")
        )
        winning_values = [int(value) for value in winning_section.split()]
        number_values = [int(value) for value in numbers_section.split()]
        self._card_winners_count[card_index] = len(
            [value for value in number_values if value in winning_values]
        )

    def _copy_card(self, card_index: int) -> None:
        for _ in range(self._card_counts[card_index]):
            for below_index in range(self._card_winners_count[card_index]):
                self._card_counts[card_index + below_index + 1] += 1

    def sum_winners(self) -> int:
        for i in range(len(self._cards)):
            self._tally_card(i)
            self._copy_card(i)
        return sum(self._card_counts.values())


if __name__ == "__main__":
    print(Scratchers("./simple_input.txt").sum_winners())
    print(Scratchers("./input.txt").sum_winners())
