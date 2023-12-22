#!/bin/env python

from collections import defaultdict
from functools import cmp_to_key


class Card:
    label: str
    value: int

    def __init__(self, label):
        self.label = label
        self.value = self._card_values[label]

    _card_values: dict[str, int] = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }


class Hand:
    _cards: list[Card]
    bet: int
    hand_strength: int

    def __init__(self, card_labels: str, bet: int):
        self._cards = [Card(label) for label in card_labels]
        self.bet = bet
        self.hand_strength = self._calculate_hand_strength()

    def _calculate_hand_strength(self) -> int:
        label_counts = defaultdict(int)
        for card in self._cards:
            label_counts[card.label] += 1
        return sum(1 << (count * 2) for count in label_counts.values())

    def get_value_of_card(self, position: int) -> int:
        return self._cards[position].value

    def __str__(self) -> str:
        return (
            "".join(card.label for card in self._cards)
            + " "
            + str(self.hand_strength)
            + " "
            + str(self.bet)
        )


class CamelCards:
    _hands = list[Hand]

    def __init__(self, file_name: str):
        with open(file_name) as input_file:
            lines = input_file.readlines()
        self._hands = [
            Hand(card_labels=line.split()[0], bet=int(line.split()[1]))
            for line in lines
        ]

    @staticmethod
    def _compare_hands(x: Hand, y: Hand) -> int:
        if x.hand_strength != y.hand_strength:
            return x.hand_strength - y.hand_strength
        for position in range(5):
            if x.get_value_of_card(position) != y.get_value_of_card(position):
                return x.get_value_of_card(position) - y.get_value_of_card(position)
        return 1

    def get_total_winnings(self) -> int:
        self._hands.sort(key=cmp_to_key(self._compare_hands))
        return sum(
            (index + 1) * self._hands[index].bet for index in range(len(self._hands))
        )


if __name__ == "__main__":
    print(CamelCards("./simple_input.txt").get_total_winnings())
    print(CamelCards("./input.txt").get_total_winnings())
