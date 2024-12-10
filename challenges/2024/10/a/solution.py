from collections import deque
from pathlib import Path
from typing import Any


def parse_input(filename: str = "input.txt") -> list[Any]:
    rv: list[Any] = []
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            rv.append([int(v) for v in line.strip()])

    return rv


src = set()
data = parse_input()


def search(data, value, row, col):
    result = []
    for _r_xfm, _c_xfm in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
        _row = row + _r_xfm
        _col = col + _c_xfm

        if _row < 0 or _col < 0:
            continue

        try:
            if data[_row][_col] == value + 1:
                result.append((data[_row][_col], _row, _col))
        except IndexError:
            ...

    return tuple(result)


mappings = {}
for row in range(len(data)):
    for col in range(len(data[row])):
        point = (data[row][col], row, col)
        mappings[point] = search(data, *point)

testme = ((0, 40, 38), ((1, 41, 38), (1, 40, 37)))
print("testing:", testme[0])


def navigate(point, accumulator):
    accumulator.update(mappings[point])
    for _point in mappings[point]:
        navigate(_point, accumulator)


total = 0
for zeropoint in [v for v in mappings.keys() if v[0] == 0]:
    descendents = set()
    descendents.add(zeropoint)
    navigate(zeropoint, descendents)

    nines = [v for v in list(descendents) if v[0] == 9]
    total += len(nines)
    print(zeropoint, len(nines), descendents)

print(total)
with open("output.txt", mode="wt") as outfile:
    outfile.write(str(""))

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(total))
