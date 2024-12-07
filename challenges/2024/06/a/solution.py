from copy import deepcopy
from pathlib import Path
from typing import Any, Literal


def parse_input(filename: str = "input.txt") -> list[Any]:
    rv: list[Any] = []
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            rv.append(list(line.strip().replace(".", " ")))

    return rv


def find_target(data: list[list[str]]):
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == "^":
                return row, col


data = parse_input()
_data = deepcopy(data)


row, col = find_target(data)
direction: Literal["up", "down", "left", "right"] = "up"
while True:
    if direction == "up":
        _row = row - 1
        _col = col
        _next_dir = "right"

    if direction == "right":
        _row = row
        _col = col + 1
        _next_dir = "down"

    if direction == "left":
        _row = row
        _col = col - 1
        _next_dir = "up"

    if direction == "down":
        _row = row + 1
        _col = col
        _next_dir = "left"

    if _row < 0 or _col < 0:
        break

    try:
        next_space = _data[_row][_col]
    except IndexError:
        break

    if next_space in ["#", "O"]:
        _row = row
        _col = col
        direction = _next_dir
    else:
        _data[_row][_col] = "·"

    row = _row
    col = _col

total = 0
with open("output.txt", mode="wt", encoding="utf-8") as outfile:
    for row in range(len(_data)):
        for col in range(len(_data[row])):
            if _data[row][col] == "·":
                total += 1

            outfile.write(_data[row][col])
        outfile.write("\n")

total += 1  # for the starting position
with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(total))
