import json
from itertools import pairwise, starmap
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append([int(i) for i in line.strip().split()])

    return rv


_input = parse_input()


def is_safe(entry: list[int]) -> bool:
    pairs = list(pairwise(entry))
    magnitude_check = sum(list(starmap(lambda x, y: 1 if (abs(y - x) < 1 or abs(y - x) > 3) else 0, pairs)))
    direction_check = sum(list(starmap(lambda x, y: int((y - x) / (abs(y - x) if (y - x) != 0 else 1)), pairs)))
    return magnitude_check == 0 and abs(direction_check) == len(list(pairs))


output = []
for entry in _input:
    status = None
    current_entry = entry
    idx = None
    for _i in range(-1, len(entry)):
        idx = _i
        if idx > -1:
            current_entry = entry[:idx] + entry[idx + 1 :]

        status = is_safe(current_entry)
        if status:
            break

    output.append((status, entry, idx, current_entry))

# for status, entry, idx, current_entry in output:
#     print(
#         "  safe" if status else "unsafe",
#         f"{json.dumps(entry): >35}",
#         f"{idx if status else ' ': >3}",
#         f"{json.dumps(current_entry if status else []): >35}",
#     )

with open("output.txt", mode="wt") as outfile:
    outfile.write(f"status| {'original entry': >33}| idx| {'modified entry': >30}|\n")
    outfile.write(f"======|{'='*34}|====|{'='*31}|\n")
    for status, entry, idx, current_entry in output:
        outfile.write("  safe" if status else "unsafe")
        outfile.write(f"{json.dumps(entry): >35}")
        outfile.write(f"{idx if status else ' ': >3}")
        outfile.write(f"{json.dumps(current_entry if status else []): >35}")
        outfile.write("\n")


with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(len([item for item in output if item[0]])))
