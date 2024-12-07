from collections import namedtuple
from copy import deepcopy
from pathlib import Path
from typing import Any, Literal, TypeAlias


def parse_input(filename: str = "input.txt") -> list[Any]:
    rv: list[Any] = []
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            rv.append(list(line.strip().replace(".", " ")))

    return rv


def find_target(data: list[list[str]]):
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == "^":
                return row, col


data = parse_input("input.txt")

Vector = namedtuple("Vector", ["row", "col", "direction"])
SENTINEL_VECTOR: Vector = Vector(-999, -999, "DONE")
Direction: TypeAlias = Literal["up", "down", "left", "right"]


class NavigationMachine:
    def __init__(
        self,
        srcmap: list[list[str]],
        /,
        initial: Vector | None = None,
        invalid_pos_chars: list[str] | str = ("#", "O"),
        traversed_char: str = "·",
        start_char: str = "^",
    ):
        self._srcmap = deepcopy(srcmap)
        self._outmap = deepcopy(srcmap)
        self._position_log = []
        self._obstacles = []
        self._invalid_pos = [*invalid_pos_chars]
        self._traversed = traversed_char
        self._start = start_char
        self._initial = initial

        if self._initial is None:
            self._initial = self._find_initial()

        self._position_log.append(self._initial)

    @property
    def output(self):
        return deepcopy(self._outmap)

    @property
    def starting(self):
        return self._initial

    @property
    def log(self):
        return deepcopy(self._position_log)

    @property
    def obstacles(self):
        return list(self._obstacles)

    @property
    def hash_output(self):
        return hash("\n".join(["".join(v) for v in self._outmap]))

    def _find_initial(self):
        for row in range(len(self._srcmap)):
            for col in range(len(self._srcmap[row])):
                if self._srcmap[row][col] == "^":
                    return Vector(row, col, "up")

        raise AttributeError("no starting point found")

    def _next(self, curr: Vector) -> Vector:
        if curr == SENTINEL_VECTOR:
            return SENTINEL_VECTOR

        row, col, direction = curr
        if direction == "up":
            _row = row - 1
            _col = col
            _next_dir = "right"

        if direction == "right":
            _row = row
            _col = col + 1
            _next_dir = "down"

        if direction == "left":
            _row = row
            _col = col - 1
            _next_dir = "up"

        if direction == "down":
            _row = row + 1
            _col = col
            _next_dir = "left"

        return Vector(_row, _col, _next_dir)

    def map_obstacle(self, curr: Vector) -> tuple[int, int] | None:
        _row, _col, _direction = self._next(curr)

        if _row < 0 or _col < 0:
            return None

        next_space = ""
        try:
            next_space = self._outmap[_row][_col]
        except IndexError:
            return None

        if next_space in self._invalid_pos:
            return None

        self._obstacles.append({curr: (_row, _col)})
        return _row, _col

    def move(self, curr: Vector) -> Vector:
        row, col, direction = curr
        _row, _col, _direction = self._next(curr)

        out_vector = None

        if _row < 0 or _col < 0:
            out_vector = SENTINEL_VECTOR

        try:
            next_space = self._srcmap[_row][_col]
        except IndexError:
            out_vector = SENTINEL_VECTOR

        if out_vector is None:
            if next_space in self._invalid_pos:
                # revert to original position
                _row = row
                _col = col

                # turn 90 degrees to the right
                direction = _direction

            elif self._srcmap[_row][_col] != self._start:
                # record where we've been
                self._outmap[_row][_col] = self._traversed

            out_vector = Vector(_row, _col, direction)

        self._position_log.append(out_vector)
        return out_vector


def is_cycle(srcmap: list[list[str]], obstacle: tuple[int, int] | None):
    if obstacle is None:
        return False, "obstacle invalid"

    visited = set()
    srcmap[obstacle[0]][obstacle[1]] = "O"
    _nm = NavigationMachine(srcmap)

    vector = _nm.starting
    while True:
        if vector == SENTINEL_VECTOR:
            return False, "navigated out"

        if vector in visited:
            return True, "found visited"

        visited.add(vector)
        vector = _nm.move(vector)


valid_obstacles = set()
nm = NavigationMachine(data)
with open("output.txt", mode="wt", encoding="utf-8") as outfile:
    count = 0
    vector = nm.starting
    outfile.write("starting outer navigation\n")
    while True:
        count += 1
        outfile.write(f"[ {count: >5} ] {vector} ...")
        if vector == SENTINEL_VECTOR:
            break

        obstacle = nm.map_obstacle(vector)
        found_cycle, cycle_msg = is_cycle(nm.output, obstacle)
        if found_cycle:
            valid_obstacles.add(obstacle)
            outfile.write(f" found cycle from obstacle: {obstacle} ({cycle_msg})")
        else:
            outfile.write(f" no cycle found from obstacle: {obstacle} ({cycle_msg})")

        vector = nm.move(vector)

        outfile.write("\n")


with open("output.map.txt", mode="wt", encoding="utf-8") as outfile:
    _data = nm.output
    for row in range(len(_data)):
        for col in range(len(_data[row])):
            outfile.write(_data[row][col])
        outfile.write("\n")

with open("output.coords.txt", mode="wt", encoding="utf-8") as outfile:
    for coord in nm.log:
        outfile.write(str(coord))
        outfile.write("\n")

with open("output.obstacles.txt", mode="wt", encoding="utf-8") as outfile:
    for coord in nm.obstacles:
        outfile.write(str(coord))
        outfile.write("\n")

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(len(valid_obstacles)))
