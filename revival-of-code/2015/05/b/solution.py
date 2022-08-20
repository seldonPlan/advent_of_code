import re
from typing import List


def parse_input(filename: str = "input.txt") -> List[str]:
    rv: List[str] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append(line.strip())

    return rv


def nice_search(check: str) -> tuple[re.Match | None, re.Match | None]:
    first = re.compile(r"([a-z][a-z])((?:.+\1)|(?:\1))")
    second = re.compile(r"([a-z]).\1")

    return first.search(check), second.search(check)


input = parse_input()

count: int = 0
for check in input:
    first, second = nice_search(check)
    if first is not None and second is not None:
        count += 1

print(count)

with open("result.txt", mode="wt") as result:
    result.write(f"{count}\n")

with open("output.txt", mode="wt") as outfile:
    for check in input:
        first, second = nice_search(check)
        outfile.write(check)
        outfile.write(" -> ")
        if first is not None:
            outfile.write(str(first.groups()))
        outfile.write(" -> ")
        if second is not None:
            outfile.write(check[second.start() : second.end()])
        outfile.write("\n")
