from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append(line.strip())

    return rv


input = parse_input()

with open("result.txt", mode="wt") as result:
    result.write(str(""))

with open("output.txt", mode="wt") as outfile:
    outfile.write(str(""))
