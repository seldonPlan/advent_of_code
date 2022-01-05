import functools
import json
import math
import sys
from typing import Dict, List, Set, Tuple

MAX_ROW: int = 99
MAX_COL: int = MAX_ROW


@functools.total_ordering
class Point(object):
    def __init__(self, row: int, column: int, value: int, seen: bool = False):
        self.row: int = row
        self.column: int = column
        self._value: int = value
        self._seen: bool = seen

        self._weight = math.inf
        self._is_start: bool = self.row == 0 and self.column == 0
        self._is_end: bool = self.row == MAX_ROW and self.column == MAX_COL

    @property
    def address(self) -> Tuple[int, int]:
        return (self.row, self.column)

    @property
    def value(self) -> int:
        return self._value

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: int):
        self._weight = float(value)

    @property
    def is_start(self) -> bool:
        return self._is_start

    @property
    def is_end(self) -> bool:
        return self._is_end

    @property
    def seen(self):
        return self._seen

    @seen.setter
    def seen(self, is_seen: bool):
        self._seen = is_seen

    def __hash__(self) -> int:
        return hash(self.address)

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Point) and self.address == __o.address

    def __repr__(self) -> str:
        rv = {
            "value": self.value,
            "is_start": self.is_start,
            "is_end": self.is_end,
            "seen": self.seen,
            "weight": int(self.weight) if self.weight != math.inf else math.inf,
        }
        return f"{repr(self.address)}: {json.dumps(rv)}"

    def __str__(self) -> str:
        return self.__repr__()

    def __lt__(self, __o) -> bool:
        if isinstance(__o, Point):
            return self.address < __o.address

        return NotImplemented


def parse_input(filename: str = "input.txt") -> Dict[Tuple[int, int], Point]:
    rv: Dict[Tuple[int, int], Point] = {}
    with open(filename, mode="rt") as inputfile:
        for row, line in enumerate(inputfile):
            for column, value in enumerate([v for v in line.strip()]):
                p = Point(row, column, int(value))
                rv[p.address] = p

    return rv


def get_neighbors(address: Tuple[int, int]) -> Set[Point]:
    neighbors: List[Tuple[int, int]] = []
    if address[0] > 0:
        neighbors.append((address[0] - 1, address[1]))

    if address[0] < MAX_ROW:
        neighbors.append((address[0] + 1, address[1]))

    if address[1] > 0:
        neighbors.append((address[0], address[1] - 1))

    if address[1] < MAX_COL:
        neighbors.append((address[0], address[1] + 1))

    return set([points[a] for a in neighbors if not points[a].seen])


def evaluate_weights():
    start = points[(0, 0)]
    start.weight = 0
    start.seen = True

    path: Set[Point] = set()

    while True:
        try:
            _w = min([p.weight for p in points.values() if p not in path])
            min_weight = int(_w) if _w != math.inf else sys.maxsize
        except ValueError:
            break

        next = [p for p in points.values() if p.weight == min_weight and p not in path]
        neighbors: Set[Point] = set()

        for point in next:
            path.add(point)
            for neighbor in get_neighbors(point.address):
                neighbors.add(neighbor)

        for point in neighbors:
            point.weight = min_weight + point.value
            point.seen = True

    return path


def find_path():
    point = points[(MAX_ROW, MAX_COL)]
    path: List[Point] = [point]

    while True:
        if point.is_start:
            break

        neighbors = get_neighbors(point.address)

        for neighbor in neighbors:
            neighbor.seen = True

        for neighbor in neighbors:
            # print(int(neighbor.weight), int(point.weight) - point.value, int(point.weight), point.value)
            if int(neighbor.weight) == int(point.weight) - point.value:
                path.append(neighbor)
                point = neighbor
                break

    return list(reversed(path))


# points = parse_input(filename="test-input.txt")
points = parse_input()


weights = evaluate_weights()
print(points[(MAX_ROW, MAX_COL)])

for point in points.values():
    point.seen = False

path = find_path()

with open("map.txt", mode="wt") as mapfile:
    for point in sorted(points.values()):
        if point in path:
            mapfile.write(f"[{point.value}]")
        else:
            mapfile.write(f" {point.value} ")

        if point.column == MAX_COL:
            mapfile.write("\n")

with open("result.txt", mode="wt") as result:
    result.write(repr(points[(MAX_ROW, MAX_COL)]))
    result.write("\n")

with open("output.txt", mode="wt") as outfile:
    for point in sorted(list(weights)):
        outfile.write(repr(point))
        outfile.write("\n")
