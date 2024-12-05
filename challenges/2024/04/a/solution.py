import re
from pathlib import Path
from typing import Any, List, Literal


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append(list(line.strip()))

    return rv


def diagonals(entries: list[list[str]], direction: Literal["upward"] | Literal["downward"]):
    seed_coords = set()

    # IMPORTANT: remember these are coordinates in a multi-dimensional array

    # diagonals can go in two directions, arbitrarily distinguished here as "upward" and "downward"

    # seed the intitial coordinates for each diagonal run
    if direction == "upward":
        for i in range(len(entries)):
            # bottom row
            seed_coords.add((len(entries) - 1, i))

    if direction == "downward":
        for i in range(len(entries)):
            # top row
            seed_coords.add((0, i))

    for i in range(len(entries)):
        # left side
        seed_coords.add((i, 0))

    # from each seeded coordinate, calculate the other coordinates in that run
    runs = []
    for x, y in seed_coords:
        curr_x, curr_y = (x, y)

        # always store the first, seeded coordinate
        run = [entries[curr_x][curr_y]]
        while True:
            try:
                # next coord depends on the diagonal direction
                if direction == "upward":
                    curr_x, curr_y = (curr_x - 1, curr_y + 1)

                if direction == "downward":
                    curr_x, curr_y = (curr_x + 1, curr_y + 1)

                # ugh... in python, negative indices are a thing
                if curr_x < 0 or curr_y < 0:
                    break

                run.append(entries[curr_x][curr_y])

            # any other index errors mean we've hit the limit
            except IndexError:
                break

        runs.append(run)

    return runs


def breakout(entries: list[list[str]]):
    runs = []

    # upward diagonal
    for entry in diagonals(entries, "upward"):
        runs.append((f"{'forward': >10}, {'upward': >10}, {'diagonal': >10}", entry))

    # downward diagonal
    for entry in diagonals(entries, "downward"):
        runs.append((f"{'forward': >10}, {'downward': >10}, {'diagonal': >10}", entry))

    # horizontal rows
    for entry in entries:
        runs.append((f"{'forward': >10}, {'horizontal': >10}, {'row': >10}", entry))

    # vertical columns
    for entry in list(zip(*entries, strict=True)):
        runs.append((f"{'forward': >10}, {'vertical': >10}, {'row': >10}", entry))

    backward_runs = []
    for run in runs:
        backward_runs.append((run[0].replace(" forward", "backward"), list(reversed(run[1]))))

    runs.extend(backward_runs)
    return runs


xmas_re = re.compile(r"XMAS")

runs = breakout(parse_input(Path(Path(__file__).parent / "input.txt")))


with open("output.txt", mode="wt") as outfile:
    for run in runs:
        outfile.write(f"{run[0]} | ")
        outfile.write(f"{len(xmas_re.findall(''.join(run[1]))): >4} | ")
        # outfile.write(json.dumps(run[1]))
        outfile.write("".join(run[1]))
        outfile.write("\n")

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(sum([len(xmas_re.findall("".join(run[1]))) for run in runs])))

# [
#     ["A", "B", "C", "D", "E"],
#     ["F", "G", "H", "I", "J"],
#     ["K", "L", "M", "N", "O"],
#     ["P", "Q", "R", "S", "T"],
#     ["U", "V", "W", "X", "Y"],
# ]

# [ [0, 0]                                 ] ["A"]
# [ [1, 0], [0, 1]                         ] ["F", "B"]
# [ [2, 0], [1, 1], [0, 2]                 ] ["K", "G", "C"]
# [ [3, 0], [2, 1], [1, 2], [0, 3]         ] ["P", "L", "H", "D"]
# [ [4, 0], [3, 1], [2, 2], [1, 3], [0, 4] ] ["U", "Q", "M", "I", "E"]
# [ [4, 1], [3, 2], [2, 3], [1, 4]         ] ["V", "R", "N", "J"]
# [ [4, 2], [3, 3], [2, 4]                 ] ["W", "S", "O"]
# [ [4, 3], [3, 4]                         ] ["X", "T"]
# [ [4, 4]                                 ] ["Y"]


# range(0, len(input))
