#!/bin/env python

import math


class Race:
    _time: int
    _distance: int

    def __init__(self, time: int, distance: int):
        self._time = time
        self._distance = distance

    def count_ways_to_win(self):
        return (
            next(
                charge_duration
                for charge_duration in reversed(range(self._time + 1))
                if self._distance_traveled(charge_duration) > self._distance
            )
            - next(
                charge_duration
                for charge_duration in range(self._time + 1)
                if self._distance_traveled(charge_duration) > self._distance
            )
            + 1
        )

    def _distance_traveled(self, charge_duration: int):
        return (self._time - charge_duration) * charge_duration


class ShortBoatRaces:
    _races = list[Race]

    def __init__(self, file_name: str):
        with open(file_name) as input_file:
            lines = input_file.readlines()
        times = lines[0].split()[1:]
        distances = lines[1].split()[1:]
        self._races = [
            Race(time=int(time), distance=int(distance))
            for time, distance in zip(times, distances)
        ]

    def get_product_of_ways_to_win(self):
        return math.prod(race.count_ways_to_win() for race in self._races)


class LongBoatRace:
    _race = list[Race]

    def __init__(self, file_name: str):
        with open(file_name) as input_file:
            lines = input_file.readlines()
        time = "".join(lines[0].split()[1:])
        distance = "".join(lines[1].split()[1:])
        self._race = Race(time=int(time), distance=int(distance))

    def get_ways_to_win(self):
        return self._race.count_ways_to_win()


if __name__ == "__main__":
    print("\nProduct of count of ways to beat record in each small race")
    print(ShortBoatRaces("./simple_input.txt").get_product_of_ways_to_win())
    print(ShortBoatRaces("./input.txt").get_product_of_ways_to_win())

    print("\nCount of ways to beat record in one big race")
    print(LongBoatRace("./simple_input.txt").get_ways_to_win())
    print(LongBoatRace("./input.txt").get_ways_to_win())
