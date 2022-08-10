from typing import Any, List, Tuple

positions: List[Any] = []
with open("input.txt", mode="rt") as input:
    positions = [int(p) for p in input.read().strip().split(",")]

output: List[Tuple[int, ...]] = []
min_fuel: Tuple[int, ...] = -1, 999999999999
for i in range(min(positions), max(positions) + 1):
    # The (a) solution was simply taking a sum of the distance travelled.
    # This assumes that the distance travelled corresponds one-to-one with the
    # fuel spent. This (b) problem adds the condition that fuel spent no longer is
    # one-to-one. The fuel spend is the "triangle number" of the distance travelled.
    # think factorial, but for addition:
    # https://math.stackexchange.com/questions/593318/factorial-but-with-addition
    # so a distance travelled of 5 means a fuel expenditure of 5 + 4 + 3 + 2 + 1 = 15
    # a handy formula for that is ((n^2) + n) / 2... (5^2 + 5) / 2 = 15
    # the only change we need to make for the (b) solution below, is to add a `map`
    # operation that introduces this new fuel calculation
    fuel: Tuple[int, ...] = i, sum(map(lambda s: int(((s * s) + s) / 2), map(lambda v: abs(i - v), positions)))
    output.append(fuel)
    if fuel[1] < min_fuel[1]:
        min_fuel = fuel

print(min_fuel)

with open("result.txt", mode="wt") as result:
    result.write(f"pos:{min_fuel[0]:> 5d} | fuel:{min_fuel[1]:> 11d}\n")

with open("output.txt", mode="wt") as outfile:
    for fuel in output:
        outfile.write(f"pos:{fuel[0]:> 5d} | fuel:{fuel[1]:> 11d}\n")
