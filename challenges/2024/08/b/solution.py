import itertools
from pathlib import Path
from typing import Any


def parse_input(filename: str = "input.txt") -> list[Any]:
    rv: list[Any] = []
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            rv.append(list(line.strip().replace(".", " ")))

    return rv


def is_valid(row, col, data):
    if row < 0 or col < 0:
        return False

    try:
        data[row][col]
    except IndexError:
        return False

    return True


def antinodes_seq(row1, col1, row2, col2, data):
    _rise = row2 - row1
    _run = col2 - col1

    _row = row1
    _col = col1
    yield _row, _col
    while True:
        _row += _rise
        _col += _run
        if not is_valid(_row, _col, data):
            break

        yield _row, _col


data = parse_input("input.txt")

output = {}
for row in range(len(data)):
    for col in range(len(data[row])):
        if data[row][col] != " ":
            if f"id_{data[row][col]}" not in output:
                output[f"id_{data[row][col]}"] = {
                    "value": data[row][col],
                    "coords": [],
                }
            output[f"id_{data[row][col]}"]["coords"].append((row, col))

all_antinodes = set()
for _k, v in output.items():
    perms = list(itertools.permutations(v["coords"], 2))
    v["perms"] = perms
    antinodes = set()
    for perm in perms:
        candidates = list(antinodes_seq(*perm[0], *perm[1], data))
        antinodes.update(candidates)
        all_antinodes.update(candidates)

    v["antinodes"] = list(antinodes)


# _debug = set()
# _debug.update(list(antinodes_seq(8, 8, 9, 9, data)))
# _debug.update(list(antinodes_seq(9, 9, 8, 8, data)))
# print(sorted(antinodes_seq(8, 8, 9, 9, data)))
# print(sorted(antinodes_seq(9, 9, 8, 8, data)))
# print(len(_debug), _debug)

with open("output.txt", mode="wt") as outfile:
    for row in data:
        outfile.write("".join(row))
        outfile.write("\n")

with open("output.mapping.txt", mode="wt") as outfile:
    for k, v in output.items():
        perms = list(itertools.permutations(v["coords"], 2))
        outfile.write(f'"{k}":\n')
        outfile.write(f'\t"value": {v["value"]},\n')
        outfile.write(f'\t"coords": {v["coords"]},\n')
        outfile.write(f'\t"perms": {v["perms"]},\n')
        outfile.write(f'\t"antinodes": {v["antinodes"]},\n')
        outfile.write("\n")

with open("output.antinodes.txt", mode="wt") as outfile:
    for row in range(len(data)):
        for col in range(len(data[row])):
            if (row, col) in all_antinodes:
                outfile.write("#")
            else:
                outfile.write(" ")
        outfile.write("\n")

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(len(all_antinodes)))
