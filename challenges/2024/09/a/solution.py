from collections import deque, namedtuple
from pathlib import Path
from typing import Any


def parse_input(filename: str = "input.txt") -> list[Any]:
    rv: list[Any] = []
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            rv.extend(list(line.strip()))

    rv.append("0")
    return [int(v) for v in rv]


def pairs(source: list[str]):
    for idx in range(0, len(source), 2):
        yield (source[idx], source[idx + 1])


ItemId = namedtuple("ItemId", ["id", "size", "spacing"])

data = parse_input("input.txt")

# populate initial mapping of src queue
#   - one ItemId for each size count
#   - one "." for each spacing count
src = deque()
tgt = deque()
spaces = deque()
for idx, item in enumerate(list(pairs(data))):
    _item = ItemId(idx, *item)

    src.extend([_item for _i in range(_item.size)])
    src.extend(["." for _i in range(_item.spacing)])

# steps in each iteration:
#   1) grab leftmost item from source (_next)
#   2) if _next is an ItemId object, then it goes next onto target, continue to next iteration
#   3) if _next is a space, then we need to grab the next rightmost non-space candidate from the src
#   4) the ItemId object from (3) goes next onto target
#   5) move to next iteration
#   6) break out of loop when there are no more items to grab from src
while True:
    _next = None
    candidate = None
    try:
        _next = src.popleft()
        if _next != ".":
            tgt.append(_next)
            continue

        spaces.append(_next)

        while True:
            candidate = src.pop()
            if candidate != ".":
                break

            spaces.append(candidate)

        tgt.append(candidate)
    except IndexError:
        break

tgt.extend(spaces)

# calculate checksum using ItemId info, and actual positional indices in the target
total = 0
for idx, item in enumerate(tgt):
    if item == ".":
        break

    total += item.id * idx

with open("output.txt", mode="wt") as outfile:
    for idx, v in enumerate(list(tgt)):
        outfile.write(f"{idx} {v}\n")
    # outfile.write(f"len(tgt) {len(tgt)}\n")

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(total))
