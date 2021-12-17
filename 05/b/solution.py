import json
from typing import List, Tuple

lines: List[List[Tuple[int, ...]]] = []
with open("input.txt", mode="rt") as input:
    for line in input:
        coords = [tuple(int(v) for v in c.split(",")) for c in line.split(" -> ")]
        lines.append(coords)
# filtered_lines = [v for v in lines if (v[0][0] == v[1][0] or v[0][1] == v[1][1] or abs(v[0][0] - v[1][0]) == abs(v[0][1] - v[1][1]))]
print("input coords:", len(lines))

# for c in lines:
#     if c[0][0] == c[1][0]:
#         print("horizontal", json.dumps(c[0]), json.dumps(c[1]))

#     if c[0][1] == c[1][1]:
#         print("vertical  ", json.dumps(c[0]), json.dumps(c[1]))

#     if abs(c[0][0] - c[1][0]) == abs(c[0][1] - c[1][1]):
#         print("diagonal  ", json.dumps(c[0]), json.dumps(c[1]))


output: List[List[int]] = [[0 for j in range(1000)] for i in range(1000)]

for coords in lines:
    start = coords[0]
    end = coords[1]

    # horizontal
    if start[0] == end[0]:
        step = -1 if start[1] > end[1] else 1
        for i in range(start[1], end[1] + step, step):
            output[start[0]][i] += 1

    # vertical
    elif start[1] == end[1]:
        step = -1 if start[0] > end[0] else 1
        for i in range(start[0], end[0] + step, step):
            output[i][start[1]] += 1

    # diagonal
    elif abs(start[0] - end[0]) == abs(start[1] - end[1]):
        step_x = -1 if start[0] > end[0] else 1
        step_y = -1 if start[1] > end[1] else 1

        x_coords = list(range(start[0], end[0] + step_x, step_x))
        y_coords = list(range(start[1], end[1] + step_y, step_y))

        for i in range(len(x_coords)):
            output[x_coords[i]][y_coords[i]] += 1

total: int = 0
for row in range(1000):
    for column in range(1000):
        if output[row][column] >= 2:
            total += 1
            # print(f"{row:> 4d},{column:> 4d}: {output[row][column]}")
print("total target overlaps:", total)
print("out of:", 1000 * 1000, "| percentage:", f"{(total / (1000 * 1000)) * 100}%")

with open("result.txt", mode="wt") as result:
    result.write(str(total) + "\n")

with open("output.txt", mode="wt") as outfile:
    for row in range(1000):
        str_row = ""
        for column in range(1000):
            str_row += f"{output[row][column]:> 2d}" if output[row][column] > 0 else "  "
        str_row += "\n"
        outfile.write(str_row)
