import re
from itertools import permutations


def parse_input(filename: str = "input.txt") -> tuple[dict[tuple[str, str], int], set[str]]:
    tokens = re.compile(r"(\w+) to (\w+) = (\d+)")

    rv: dict[tuple[str, str], int] = {}
    locations: set[str] = set()
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            m = tokens.match(line.strip())
            if m is None:
                raise Exception(f"unable to parse line [{line}]")
            locations.add(m[1])
            locations.add(m[2])
            rv[(m[1], m[2])] = int(m[3])
            rv[(m[2], m[1])] = int(m[3])
    return rv, locations


loc_map, locations = parse_input()
paths = [v for v in permutations(locations)]
weights: list[list[int]] = []

max: tuple[int, tuple[str, ...]] = 0, ()
for p in paths:
    w: list[int] = [0]
    w.extend([loc_map[p[i - 1 : i + 1]] for i in range(1, len(p), 1)])  # type: ignore
    weights.append(w)
    if sum(w) > max[0]:
        max = sum(w), p

print(*max)

with open("result.txt", mode="wt") as result:
    result.write(str(max[0]))

with open("output.txt", mode="wt") as outfile:
    for p in paths:
        w = [0]
        w.extend([loc_map[p[i - 1 : i + 1]] for i in range(1, len(p), 1)])  # type: ignore
        outfile.write(f"{sum(w): 4d} -> {str(p)}\n")
