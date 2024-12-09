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


def concat(a: int, b: int):
    return int(str(a) + str(b))


src_ops = [("+", op.add), ("*", op.mul), ("||", concat)]
data = parse_input("input.txt")
results = {item: [] for item in data}
total_data_count = len(data)
count = 0
for item in data:
    count += 1
    print(f"working on [{count:0>4}] out of [{total_data_count:0>4}]")

    # trinary representation of upper limit
    upper_limit_trinary = "2" * (len(item[1]) - 1)
    upper_limit = int(upper_limit_trinary, 3)

    # all operation sequences corresponding to the cartesian product of (0, 1, 2) across all trits in upper limit
    # 0 is the first op, 1 is the second op
    # each sequence is one possible permutation of all possible operations that could be run
    ops_seq = [[src_ops[idx] for idx in t] for t in list(itertools.product(range(3), repeat=len(upper_limit_trinary)))]

    for ops in ops_seq:
        commands = deque([v[1] for v in ops])
        acc = list(itertools.accumulate(item[1], lambda left, right: commands.pop()(left, right)))  # noqa: B023

        if acc[len(item[1]) - 1] == item[0]:
            results[item].append([v[0] for v in ops])
            break


with open("output.txt", mode="wt") as outfile:
    for k, v in results.items():
        outfile.write(f"{k}: ")
        outfile.write(f"{v}\n")

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(sum([t[0][0] for t in results.items() if len(t[1]) > 0])))
