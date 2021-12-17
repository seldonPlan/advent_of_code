import json
from typing import Any, List

lines: List[Any] = []
with open("input.txt", mode="rt") as inputfile:
    lines = [i.strip() for i in inputfile.readlines()]


# do stuff

with open("result.txt", mode="wt") as result:
    result.write(str(""))

with open("output.json", mode="wt") as outfile:
    outfile.write(json.dumps({}))
