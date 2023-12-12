#!/bin/env python

class AlmanacMap:
    source_start: int
    destination_start: int
    range: int

    def __init__(self, source_start: int, destination_start: int, range: int):
        self.source_start = source_start
        self.destination_start = destination_start
        self.range = range

    def __repr__(self):
        return f"<src: {self.source_start} dst: {self.destination_start} range: {self.range}>"


class Almanac:
    _seeds: list[int]
    _map_sequence: list[list[AlmanacMap]]
    _collapsed_map: list[AlmanacMap]

    def __init__(self, file_name: str):
        with open(file_name) as input_file:
            self._seeds = [
                int(seed) for seed in input_file.readline().split(":")[1].split()
            ]
            if input_file.readline().rsplit():
                raise RuntimeError("Expected blank line after seed list")

            self._map_sequence = list()
            while line := input_file.readline():
                if line.split()[1] != "map:":
                    raise RuntimeError("Expected to find almanac section header")
                map_entries: list[AlmanacMap] = list()
                while mapping := input_file.readline().rstrip():
                    values = mapping.split()
                    map_entries.append(
                        AlmanacMap(
                            source_start=int(values[1]),
                            destination_start=int(values[0]),
                            range=int(values[2]),
                        )
                    )
                self._map_sequence.append(map_entries)
        self._build_ranges()

    def _build_ranges(self) -> int:
        """
        Instead of trying to map every value discretely to an output, treat it continuously. Figure
        out the boundaries lay where changing the input by 1 jumps to a different place in the map.

        This requires working backwards from the final map, subdividing the input into ranges based
        on where the output changes to a new range.

        Once we have a list of all ranges, run those boundaries through the maps in the forward
        direction to determine what input ranges map to which output ranges.
        """

        current_range_boundaries: list[int] = []
        for map in reversed(self._map_sequence):
            last_range_boundaries = current_range_boundaries
            current_range_boundaries = [
                next(
                    (
                        value
                        for x in map
                        if (
                            value := self._get_value_if_in_range_backwards(
                                last_range_boundary, x
                            )
                        )
                    ),
                    last_range_boundary,
                )
                for last_range_boundary in last_range_boundaries
            ] + [map_segment.source_start for map_segment in map]
            current_range_boundaries.sort()
        self._collapsed_map = []
        current_range_boundaries.sort()
        for i in range(len(current_range_boundaries) - 1):
            self._collapsed_map.append(
                AlmanacMap(
                    source_start=current_range_boundaries[i],
                    destination_start=self._calculate_location(
                        current_range_boundaries[i]
                    ),
                    range=current_range_boundaries[i + 1] - current_range_boundaries[i],
                )
            )

        self._collapsed_map.sort(key=lambda x: x.destination_start)

    @staticmethod
    def _get_value_if_in_range(
        source_value: int, almanac_map: AlmanacMap
    ) -> int | None:
        stuff = (
            almanac_map.destination_start + (source_value - almanac_map.source_start)
            if source_value >= almanac_map.source_start
            and source_value - almanac_map.source_start < almanac_map.range
            else None
        )
        return stuff

    @staticmethod
    def _get_value_if_in_range_backwards(
        source_value: int, almanac_map: AlmanacMap
    ) -> int | None:
        stuff = (
            almanac_map.source_start + (source_value - almanac_map.destination_start)
            if source_value >= almanac_map.destination_start
            and source_value - almanac_map.destination_start < almanac_map.range
            else None
        )
        return stuff

    def _calculate_location(self, source_value: int) -> int:
        current_value = source_value
        for map in self._map_sequence:
            current_value = next(
                (
                    value
                    for x in map
                    if (value := self._get_value_if_in_range(current_value, x))
                ),
                current_value,
            )
        return current_value

    def get_closest_seed_from_individuals(self) -> int:
        return min(self._calculate_location(x) for x in self._seeds)

    @staticmethod
    def _get_min_value_from_overlap(
        source_value_start: int, range: int, almanac_map: AlmanacMap
    ) -> int | None:
        if (source_value_start + range) < almanac_map.source_start:
            return None
        if source_value_start <= almanac_map.source_start:
            return almanac_map.destination_start
        elif source_value_start <= (almanac_map.source_start + almanac_map.range):
            return almanac_map.destination_start + (
                source_value_start - almanac_map.source_start
            )
        return None

    def _calculate_location_from_range(self, source_value: int, range: int) -> int:
        return min(
            value
            for x in self._collapsed_map
            if (value := self._get_min_value_from_overlap(source_value, range, x))
        )

    def get_closest_seed_from_ranges(self) -> int:
        return min(
            self._calculate_location_from_range(start, count)
            for start, count in zip(*[iter(self._seeds)] * 2)
        )


if __name__ == "__main__":
    print("\nClosest from seed individual")
    print(Almanac("./simple_input.txt").get_closest_seed_from_individuals())
    print(Almanac("./input.txt").get_closest_seed_from_individuals())

    print("\nClosest from seed ranges")
    print(Almanac("./simple_input.txt").get_closest_seed_from_ranges())
    print(Almanac("./input.txt").get_closest_seed_from_ranges())
