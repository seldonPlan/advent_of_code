import re
from itertools import starmap
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: str = None
    with open(filename, mode="rt") as inputfile:
        rv = inputfile.read()

    # per problem description, the input always starts with an implied "do()"
    return ("do()" + rv).replace("\n", "")


# non overlapping version of pairwise
def pairs(source: list[str]):
    for idx in range(0, len(source), 2):
        yield (source[idx], source[idx + 1])


# run the solution for (a) on every pair that starts with "do()"
def sumpair(condition: str, source: str):
    if condition == "do()":
        return sum(list(starmap(lambda left, right: int(left) * int(right), mul_re.findall(source))))

    return 0


input = parse_input()

mul_re = re.compile(r"mul\((?P<left_op>\d{1,3}),(?P<right_op>\d{1,3})\)")
conditional_re = re.compile(r"(?P<conditional>do(?:n't)?\(\))")

# increment the running total from each pair
total = 0
for pair in list(pairs(conditional_re.split(input)[1:])):
    total += sumpair(*pair)

with open("result.txt", mode="wt") as result:
    result.write(str(total))

with open("output.txt", mode="wt") as outfile:
    import json

    outfile.write(json.dumps(list(pairs(conditional_re.split(input)[1:])), indent=4))
