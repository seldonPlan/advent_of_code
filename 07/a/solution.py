from typing import Any, List, Tuple

positions: List[Any] = []
with open("input.txt", mode="rt") as input:
    positions = [int(p) for p in input.read().strip().split(",")]

output: List[Tuple[int, ...]] = []
min_fuel: Tuple[int, ...] = -1, 999999999999
for i in range(min(positions), max(positions) + 1):
    fuel: Tuple[int, ...] = i, sum(map(lambda v: abs(i - v), positions))
    output.append(fuel)
    if fuel[1] < min_fuel[1]:
        min_fuel = fuel

print(min_fuel)

with open("result.txt", mode="wt") as result:
    result.write(f"pos:{min_fuel[0]:> 5d} | fuel:{min_fuel[1]:> 8d}\n")

with open("output.txt", mode="wt") as outfile:
    for fuel in output:
        outfile.write(f"pos:{fuel[0]:> 5d} | fuel:{fuel[1]:> 8d}\n")
