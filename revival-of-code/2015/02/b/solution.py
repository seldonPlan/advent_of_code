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
    short_sides = sum([2 * s for s in sorted(i)[:2]])
    volume = i[0] * i[1] * i[2]
    total += short_sides + volume
    print(i, short_sides, volume, short_sides + volume)

print("total:", total)
with open("result.txt", mode="wt") as result:
    result.write(f"{total}\n")

with open("output.txt", mode="wt") as outfile:
    for i in input:
        short_sides = sum([2 * s for s in sorted(i)[:2]])
        volume = i[0] * i[1] * i[2]
        total = short_sides + volume
        outfile.write(f"l: {i[0]: >2d}, w: {i[1]: >2d}, h: {i[2]: >2d}")
        outfile.write(" --> ")
        outfile.write(f"short sides: {str(sorted(i)[:2]): >8}")
        outfile.write(" --> ")
        outfile.write(f"volume: {volume: >6d}")
        outfile.write(" --> ")
        outfile.write(f"total: {total: >6d}\n")
