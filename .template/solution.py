from pathlib import Path
from typing import Any


def parse_input(filename: str = "input.txt") -> list[Any]:
    rv: list[Any] = []
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            rv.append(line.strip())

    return rv


data = parse_input()

with open("output.txt", mode="wt") as outfile:
    outfile.write(str(""))

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(""))
