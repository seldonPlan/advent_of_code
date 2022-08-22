import json
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append(line.strip())

    return rv


input = parse_input()

total: int = 0
for i in input:
    # the built in json encoder does all the work here...
    total += len(json.JSONEncoder().encode(i)) - len(i)

print(total)

with open("result.txt", mode="wt") as result:
    result.write(str(total))

with open("output.txt", mode="wt") as outfile:
    for i in input:
        outfile.write(" -> ".join([i, json.JSONEncoder().encode(i)]))
        outfile.write(" | ")
        outfile.write(f"{len(json.JSONEncoder().encode(i))} - {len(i)} = {len(json.JSONEncoder().encode(i)) - len(i)}")
        outfile.write("\n")
