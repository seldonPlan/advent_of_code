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


def populate_points(points: Tuple[Tuple[int, int], ...]):
    max_x: int = 0
    max_y: int = 0
    for i in points:
        max_x = max([max_x, i[0]])
        max_y = max([max_y, i[1]])

    rv: List[List[bool]] = []
    for row in range(max_x + 1):
        rv.append([False] * (max_y + 1))

    for x, y in points:
        rv[x][y] = True

    return rv


def do_fold(input: List[List[bool]], direction: str, fold: int):
    a: List[List[bool]] = []
    b: List[List[bool]] = []
    rv: List[List[bool]] = []

    if direction == "x":
        a = input[0:fold]
        b = list(reversed(input[fold + 1 :]))
    if direction == "y":
        for i in range(len(input)):
            a.append(input[i][0:fold])
            b.append(list(reversed(input[i][fold + 1 :])))

    # init output array
    for row in range(len(a)):
        rv.append([False] * len(a[0]))

    # perform calculation
    for x in range(len(a)):
        for y in range(len(a[0])):
            rv[x][y] = a[x][y] or b[x][y]

    return rv


points_array = do_fold(populate_points(input[0]), input[1][0][0], input[1][0][1])

print(sum([len([s for s in r if s]) for r in points_array]))

with open("result.txt", mode="wt") as result:
    result.write(f"total points after first fold: {sum([len([s for s in r if s]) for r in points_array])}\n")

with open("output.txt", mode="wt") as outfile:
    for r in points_array:
        outfile.write("".join(["*" if i else " " for i in r]))
        outfile.write(str("\n"))
