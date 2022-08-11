import json
from typing import Any, List

lines: List[int] = []
with open("input.txt", mode="rt") as input:
    lines = [int(i) for i in input.readlines()]

compare: int = lines[0]

output: List[Any] = []
output.append({"idx": 0, "value": compare, "result": None})

increase_count: int = 0

for i in range(1, len(lines)):
    _rv: Any = {"idx": i, "value": lines[i], "result": None}
    if lines[i] > compare:
        _rv["result"] = "INCREASED"
        increase_count += 1

    elif lines[i] < compare:
        _rv["result"] = "DECREASED"

    elif lines[i] == compare:
        _rv["result"] = "EQUAL"

    output.append(_rv)
    compare = lines[i]

print(increase_count, len([r for r in output if r["result"] == "INCREASED"]))

with open("result.txt", mode="wt") as result:
    result.write(str(increase_count))

with open("output.json", mode="wt") as outfile:
    outfile.write(json.dumps(output))
