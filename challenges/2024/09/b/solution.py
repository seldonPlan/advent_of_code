from collections import deque, namedtuple
from pathlib import Path
from typing import Any, Literal


def parse_input(filename: str = "input.txt") -> list[Any]:
    rv: list[Any] = []
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            rv.extend(list(line.strip()))

    rv.append("0")
    return [int(v) for v in rv]


def make_pairs(source: list[str]):
    for idx in range(0, len(source), 2):
        yield (source[idx], source[idx + 1])


ItemId = namedtuple("ItemId", ["id", "size", "spacing"])

data = parse_input("input.txt")
# print(data, list(make_pairs(data)), sep="\n")


class ItemWalker:
    def __init__(self, pairs: list[tuple[int, int]]):
        self._data: list[ItemId | Literal["."]] = []

        for idx, item in enumerate(pairs):
            _item = ItemId(idx, *item)

            self._data.extend([_item for _i in range(_item.size)])
            self._data.extend(["." for _i in range(_item.spacing)])

        self._src = tuple(self._data)
        self.right_cursor = (len(self._data) - 1, max([item.id for item in self._data if item != "."]))
        self.left_cursor = 0

    @property
    def src(self):
        return self._src

    @property
    def tgt(self):
        return tuple(self._data)

    def walk(self):
        while True:
            item, item_coords = self.next_item_candidate()
            space_coords = self.next_space_candidate(item.size)

            if len(space_coords) == len(item_coords) and max(space_coords) < min(item_coords):
                # print(
                #     "candidate item ",
                #     item,
                #     " | right side item coords ",
                #     item_coords,
                #     " | left side space coords ",
                #     space_coords,
                #     sep="",
                # )
                self.swap(space_coords, item_coords)

            if item.id == 0:
                break

    def next_item_candidate(self):
        for idx in range(self.right_cursor[0], 0, -1):
            candidate = self._data[idx]
            if candidate != "." and candidate.id == self.right_cursor[1]:
                self.right_cursor = (idx - candidate.size, self.right_cursor[1] - 1)
                return candidate, tuple(sorted(range(idx, idx - candidate.size, -1)))

    def next_space_candidate(self, size):
        run = []
        for idx in range(len(self._data)):
            if self._data[idx] == ".":
                run.append(idx)
                if len(run) == size:
                    return tuple(run)

                continue

            run = []

        return ()

    def swap(self, space_coords, item_coords):
        for coords in zip(space_coords, item_coords, strict=True):
            _c = self._data[coords[0]]
            self._data[coords[0]] = self._data[coords[1]]
            self._data[coords[1]] = _c


iw = ItemWalker(list(make_pairs(data)))
# iw.walk()
# print("".join([str(v.id) if v != "." else v for v in iw.src]))
# print("".join([str(v.id) if v != "." else v for v in iw.tgt]))

with open("output.txt", mode="wt") as outfile:
    while True:
        item, item_coords = iw.next_item_candidate()
        space_coords = iw.next_space_candidate(item.size)

        outfile.write(f"candidate item: {item} | ")
        outfile.write(f"right side item coords: {item_coords} | ")
        outfile.write(f"left side space coords: {space_coords}\n")

        if len(space_coords) == len(item_coords) and max(space_coords) < min(item_coords):
            iw.swap(space_coords, item_coords)

        if item.id == 0:
            break

# calculate checksum using ItemId info, and actual positional indices in the target
total = 0
for idx, item in enumerate(iw.tgt):
    if item == ".":
        continue

    total += item.id * idx

with open("output.src.txt", mode="wt") as outfile:
    outfile.write("".join([str(v.id) if v != "." else v for v in iw.src]))
    outfile.write("\n")

with open("output.tgt.txt", mode="wt") as outfile:
    outfile.write("".join([str(v.id) if v != "." else v for v in iw.tgt]))
    outfile.write("\n")

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(total))
