import json
from pathlib import Path
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            rv.append(list(line.strip()))

    return rv


data = parse_input("input.txt")


def check_candidate(candidate: list[list[str]]):
    # disqualify if the middle value is not "A"
    if candidate[1][1] != "A":
        return False

    # an "A" or "X" in any corner disqualifies the match
    # fmt: off
    if "A" in [candidate[0][0], candidate[0][2], candidate[2][0], candidate[2][2]] \
    or "X" in [candidate[0][0], candidate[0][2], candidate[2][0], candidate[2][2]] :
        # fmt: on
        return False

    # opposite corners should have different values from each other
    # only four total possible values, "A", "X", "M", "S", and we have already excluded "A" and "X"
    return candidate[0][0] != candidate[2][2] and candidate[0][2] != candidate[2][0]


total = 0
with open("output.txt", mode="wt") as outfile:
    for row in range(1, len(data) - 1):
        for col in range(1, len(data[row]) - 1):
            candidate = [
                data[row - 1][col - 1 : col + 2],
                data[row][col - 1 : col + 2],
                data[row + 1][col - 1 : col + 2],
            ]

            if check_candidate(candidate):
                total += 1
                outfile.write("match | ")
                outfile.write(f"center ({row: >3}, {col: >3}) | ")
                outfile.write(json.dumps(candidate))
                outfile.write("\n")

    outfile.write(f"found [{total}] matches")

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(total))
