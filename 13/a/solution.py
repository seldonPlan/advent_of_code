from typing import List, Tuple


def parse_input(filename: str = "input.txt") -> Tuple[Tuple[Tuple[int, int], ...], Tuple[Tuple[str, int], ...]]:
    points: List[Tuple[int, int]] = []
    folds: List[Tuple[str, int]] = []
    with open(filename, mode="rt") as inputfile:
        o = inputfile.read().split("\n\n")
        for point_str in o[0].split("\n"):
            _p = point_str.strip().split(",")
            points.append((int(_p[0]), int(_p[1])))

        for folds_str in o[1].split("\n"):
            if len(folds_str.strip()) > 0:
                _f = folds_str.strip().split(" ")[2].split("=")
                folds.append((_f[0], int(_f[1])))
    return tuple(points), tuple(folds)


input = parse_input()
print(input[0])
print(input[1])

with open("result.txt", mode="wt") as result:
    result.write(str(""))

with open("output.txt", mode="wt") as outfile:
    outfile.write(str(""))
