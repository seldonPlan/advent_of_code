import re
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append(line.strip())

    return rv


# identify each token, escape sequences and valid individual chars
tokens = re.compile(r'(\\x[0-9a-f]{2})|(\\")|(\\\\)|([a-z])')
input = parse_input()

total: int = 0
for i in input:
    # first and last `"` are a part of every line, and wont be counted in the "in memory" count
    m = tokens.findall(i[1:-1])
    print(i, len(i), len(m), len(i) - len(m))
    total += len(i) - len(m)

print(total)

with open("result.txt", mode="wt") as result:
    result.write(str(total))

with open("output.txt", mode="wt") as outfile:
    for i in input:
        m = tokens.findall(i[1:-1])
        outfile.write(" | ".join([i, f"{len(i)} - {len(m)} = {len(i) - len(m)}"]))
        outfile.write("\n")
