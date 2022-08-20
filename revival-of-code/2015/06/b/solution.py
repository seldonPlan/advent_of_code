import re
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    check = re.compile(r"(?:turn )?(on|off|toggle) (\d+),(\d+) through (\d+),(\d+)")
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            m = check.match(line.strip())
            if m is None:
                raise Exception(f"unexpected line:\n{line}\n")
            parsed = m.groups()
            rv.append((parsed[0], (int(parsed[1]), int(parsed[2])), (int(parsed[3]), int(parsed[4]))))

    return rv


def command(state, op: str, c1: tuple[int, int], c2: tuple[int, int]):
    for row in range(1000):
        if row < c1[0]:
            continue

        if row > c2[0]:
            break

        for col in range(1000):
            if col >= c1[1] and col <= c2[1]:
                match op:
                    case "on":
                        state[row][col] += 1
                    case "off":
                        state[row][col] -= 1
                        if state[row][col] < 0:
                            state[row][col] = 0
                    case "toggle":
                        state[row][col] += 2
                    case _:
                        raise Exception(f"unexpected op [{op}]")


state: list[list[int]] = []
for _ in range(1000):
    r = []
    for _ in range(1000):
        r.append(0)
    state.append(r)

input = parse_input()


for i in input:
    command(state, i[0], i[1], i[2])

count: int = 0
for row in range(1000):
    for col in range(1000):
        count += state[row][col]

print(count)
with open("result.txt", mode="wt") as result:
    result.write(str(count))

with open("output.txt", mode="wt") as outfile:
    for row in range(1000):
        for col in range(1000):
            outfile.write(f"{state[row][col]: >3d}")

        outfile.write("\n")
