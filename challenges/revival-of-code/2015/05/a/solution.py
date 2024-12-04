from typing import List


def parse_input(filename: str = "input.txt") -> List[str]:
    rv: List[str] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append(line.strip())

    return rv


def is_nice(check: str) -> bool:
    vowels: int = 0
    double: bool = False
    naughty: bool = False

    for i in range(len(check)):
        vowels += 1 if check[i] in "aeiou" else 0
        if i == 0:
            continue

        if check[i - 1] == check[i]:
            double = True

        if check[i - 1 : i + 1] in ["ab", "cd", "pq", "xy"]:
            naughty = True

    return vowels >= 3 and double and not naughty


input = parse_input()

print(sum([int(is_nice(check)) for check in input]))

with open("result.txt", mode="wt") as result:
    result.write(f"{sum([int(is_nice(check)) for check in input])}\n")

with open("output.txt", mode="wt") as outfile:
    for check in input:
        outfile.write(check)
        outfile.write(" -> ")
        outfile.write("nice" if is_nice(check) else "naughty")
        outfile.write("\n")
