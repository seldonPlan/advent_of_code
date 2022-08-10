import json
from typing import Any, List

bits: List[Any] = []
with open("input.txt", mode="rt") as input:
    for idx, line in enumerate(input):
        _values = [int(i) for i in line.strip()]
        bits.append({"idx": idx, "value": _values})


output: List[int] = [0 for b in bits[0]["value"]]

for b in bits:
    for idx, bit in enumerate(b["value"]):
        output[idx] += bit

gamma: int = int("".join([("1" if o > 500 else "0") for o in output]), base=2)
epsilon: int = int("".join([("1" if o < 500 else "0") for o in output]), base=2)

print("gamma:", gamma, "epsilon:", epsilon)
print("power consumption:", gamma * epsilon)

with open("result.txt", mode="wt") as result:
    result.write(f"gamma: {gamma}\n")
    result.write(f"epsilon: {epsilon}\n")
    result.write(f"power consumption: {gamma * epsilon}\n")

with open("output.json", mode="wt") as outfile:
    outfile.write(json.dumps(output))
