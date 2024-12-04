import re
from itertools import starmap
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: str = None
    with open(filename, mode="rt") as inputfile:
        rv = inputfile.read()

    return rv


mul_re = re.compile(r"mul\((?P<left_op>\d{1,3}),(?P<right_op>\d{1,3})\)")
input = parse_input()

with open("result.txt", mode="wt") as result:
    result.write(str(sum(list(starmap(lambda left, right: int(left) * int(right), mul_re.findall(input))))))

with open("output.txt", mode="wt") as outfile:
    import json

    outfile.write(json.dumps(mul_re.findall(input)))
    outfile.write("\n")
    outfile.write("=" * 80)
    outfile.write("\n")
    outfile.write(json.dumps(list(starmap(lambda left, right: int(left) * int(right), mul_re.findall(input)))))
    outfile.write("\n")
    outfile.write("=" * 80)
    outfile.write("\n")
    outfile.write(str(sum(list(starmap(lambda left, right: int(left) * int(right), mul_re.findall(input))))))
