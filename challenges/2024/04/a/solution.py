import json
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append(list(line.strip()))

    return rv


input = parse_input()
diagonals = []
for i in range(len(input)):
    letter_run = []
    for j in range(i + 1):
        letter_run.append(input[i][j])


[print(json.dumps(a)) for a in input]

with open("output.txt", mode="wt") as outfile:
    outfile.write(str(""))

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(""))
    resultfile.write(str(""))

[
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "J"],
    ["K", "L", "M", "N", "O"],
    ["P", "Q", "R", "S", "T"],
    ["U", "V", "W", "X", "Y"],
]

# [ [0, 0]                                 ] ["A"]
# [ [1, 0], [0, 1]                         ] ["F", "B"]
# [ [2, 0], [1, 1], [0, 2]                 ] ["K", "G", "C"]
# [ [3, 0], [2, 1], [1, 2], [0, 3]         ] ["P", "L", "H", "D"]
# [ [4, 0], [3, 1], [2, 2], [1, 3], [0, 4] ] ["U", "Q", "M", "I", "E"]
# [ [4, 1], [3, 2], [2, 3], [1, 4]         ] ["V", "R", "N", "J"]
# [ [4, 2], [3, 3], [2, 4]                 ] ["W", "S", "O"]
# [ [4, 3], [3, 4]                         ] ["X", "T"]
# [ [4, 4]                                 ] ["Y"]


# range(0, len(input))


# for i in range(len(a)):
#     coords.add((i, 0))

# for i in range(len(a)):
#     coords.add((len(a) - 1, i))

# runs = []
# for x, y in coords:
#     current_val = (x, y)
#     end_val = (y, x)
#     run = [current_val]
#     while current_val != end_val:
#         _x, _y = current_val
#         current_val = (_x - 1, _y + 1)
#         run.append(current_val)
#     runs.append(run)
