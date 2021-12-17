import json
from typing import Any, List

lines: List[int] = []
with open("input.txt", mode="rt") as input:
    lines = [int(i) for i in input.readlines()]

compare: int = lines[0] + lines[1] + lines[2]

output: List[Any] = []
output.append({"idx": 0, "agg": None, "value": lines[0], "result": None})
output.append({"idx": 1, "agg": None, "value": lines[1], "result": None})
output.append({"idx": 2, "agg": compare, "value": lines[2], "result": None})

increase_count: int = 0

for i in range(3, len(lines)):
    _agg: int = lines[i] + lines[i - 1] + lines[i - 2]
    _rv: Any = {"idx": 0, "agg": _agg, "value": lines[i], "result": None}
    if _agg > compare:
        _rv["result"] = "INCREASED"
        increase_count += 1

    elif _agg < compare:
        _rv["result"] = "DECREASED"

    elif _agg == compare:
        _rv["result"] = "EQUAL"

    output.append(_rv)
    compare = _agg

print(increase_count, len([r for r in output if r["result"] == "INCREASED"]))

with open("result.txt", mode="wt") as result:
    result.write(str(increase_count))

with open("output.json", mode="wt") as outfile:
    outfile.write(json.dumps(output))
