from collections import namedtuple
from typing import Dict, Tuple

Point = namedtuple("Point", ["value", "row", "column"])


def parse_input(filename: str = "test-input.txt") -> Dict[Tuple[int, ...], Point]:
    rv: Dict[Tuple[int, ...], Point] = {}
    with open(filename, mode="rt") as inputfile:
        for row, line in enumerate(inputfile):
            for column, value in enumerate([v for v in line.strip()]):
                rv[(row, column)] = Point(int(value), row, column)

    return rv


input = parse_input()
print({(v.row, v.column): v for v in input.values() if v.row == 0})

with open("result.txt", mode="wt") as result:
    result.write(str(""))

with open("output.txt", mode="wt") as outfile:
    outfile.write(str(""))
