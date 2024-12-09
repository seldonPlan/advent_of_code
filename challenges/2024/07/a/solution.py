import itertools
import operator as op
from collections import deque
from pathlib import Path
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            _line = line.strip().split(":")
            rv.append((int(_line[0].strip()), tuple([int(v.strip()) for v in _line[1].strip().split(" ")])))

    return rv


src_ops = [("+", op.add), ("*", op.mul)]
data = parse_input("input.txt")
results = {item: [] for item in data}
for item in data:
    # binary representation of upper limit
    upper_limit = int("1" * (len(item[1]) - 1), 2)

    # all operation sequences corresponding to the cartesian product of (0, 1) across all bits in upper limit
    # 0 is the first op, 1 is the second op
    # each sequence is one possible permutation of all possible operations that could be run
    ops_seq = [[src_ops[idx] for idx in t] for t in list(itertools.product(range(2), repeat=upper_limit.bit_length()))]

    for ops in ops_seq:
        commands = deque([v[1] for v in ops])
        acc = list(itertools.accumulate(item[1], lambda left, right: commands.pop()(left, right)))  # noqa: B023

        if acc[len(item[1]) - 1] == item[0]:
            results[item].append([v[0] for v in ops])


with open("output.txt", mode="wt") as outfile:
    for k, v in results.items():
        outfile.write(f"{k}: ")
        outfile.write(f"{v}\n")

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(sum([t[0][0] for t in results.items() if len(t[1]) > 0])))
