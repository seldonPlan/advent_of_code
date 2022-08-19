from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[tuple[int, ...]]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append(tuple([int(v) for v in line.strip().split("x")]))

    return rv


input = parse_input()
total: int = 0
for i in input:
    sides = (2 * i[0] * i[1], 2 * i[0] * i[2], 2 * i[1] * i[2])
    total += sum([*sides, int(min(sides) / 2)])
    # print(i, sides, min(sides), sum([*sides, int(min(sides) / 2)]))

print("total:", total)
with open("result.txt", mode="wt") as result:
    result.write(f"{total}\n")

with open("output.txt", mode="wt") as outfile:
    for i in input:
        sides = (2 * i[0] * i[1], 2 * i[0] * i[2], 2 * i[1] * i[2])
        total = sum([*sides, int(min(sides) / 2)])
        outfile.write(f"l: {i[0]: >2d}, w: {i[1]: >2d}, h: {i[2]: >2d}")
        outfile.write(" --> ")
        outfile.write(f"2*l*w: {sides[0]: >4d}, 2*l*h: {sides[1]: >4d}, 2*w*h: {sides[2]: >4d}")
        outfile.write(" --> ")
        outfile.write(f"smallest side: {int(min(sides) / 2): >4d}")
        outfile.write(" --> ")
        outfile.write(f"total: {total: >4d}\n")
