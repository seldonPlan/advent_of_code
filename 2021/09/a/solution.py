from typing import List, Tuple

floor_map: List[List[int]] = []
with open("input.txt", mode="rt") as inputfile:
    for line in inputfile:
        floor_map.append([int(h) for h in line.split()[0]])
limits: Tuple[int, int] = (len(floor_map) - 1, len(floor_map[0]) - 1)


def is_local_minimum(row, column):
    #                      [top, bottom, left, right, value]
    positions: List[int] = [99, 99, 99, 99, floor_map[row][column]]

    # avoid edge cases
    if row > 0:
        # top
        positions[0] = floor_map[row - 1][column]

    if row < limits[0]:
        # bottom
        positions[1] = floor_map[row + 1][column]

    if column > 0:
        # left
        positions[2] = floor_map[row][column - 1]

    if column < limits[1]:
        # right
        positions[3] = floor_map[row][column + 1]

    if all(map(lambda v: v == floor_map[row][column] or v == 99, [v for v in positions[:4]])):
        return (False, positions)

    return (floor_map[row][column] == min(positions), positions)


output: List[Tuple[int, ...]] = []
for row, columns in enumerate(floor_map):
    for column, value in enumerate(columns):
        is_min, positions = is_local_minimum(row, column)
        if is_min:
            output.append((row, column, value, positions))

print(len(output), sum([(i[2] + 1) for i in output]))

with open("result.txt", mode="wt") as result:
    result.write(f"total low points: {len(output)}\n")
    result.write(f"total risk score: {sum([(i[2] + 1) for i in output])}\n")

with open("output.txt", mode="wt") as outfile:
    for low_point in output:
        outfile.write(repr(low_point))
        outfile.write("\n")
