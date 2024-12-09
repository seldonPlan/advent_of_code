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

data = parse_input("input.example.txt")

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


def fetch_next(q):
    _items = []
    _spaces = []

    while True:
        candidate = q.pop()
        if candidate == ".":
            _spaces.append(candidate)
            continue

        break

    _items.append(candidate)
    for _i in range(candidate.size - 1):
        _checkme = q.pop()
        assert _checkme == candidate
        _items.append(_checkme)

    return _items, _spaces


print(fetch_next(src))
print(fetch_next(src))
print(fetch_next(src))
print(fetch_next(src))
print(fetch_next(src))
print(fetch_next(src))
print(fetch_next(src))
print(fetch_next(src))
print(fetch_next(src))
print(fetch_next(src))

# calculate checksum using ItemId info, and actual positional indices in the target
total = 0
for idx, item in enumerate(tgt):
    if item == ".":
        break

    total += item.id * idx

# with open("output.txt", mode="wt") as outfile:
#     for idx, v in enumerate(list(tgt)):
#         outfile.write(f"{idx} {v}\n")
#     # outfile.write(f"len(tgt) {len(tgt)}\n")

# with open("result.txt", mode="wt") as resultfile:
#     resultfile.write(str(total))
