from collections import namedtuple
from typing import Dict, List, NamedTuple, Optional, Tuple

coordinates: NamedTuple = namedtuple("coordinates", ["row", "col"])


class Octopus(object):
    def __init__(self, coords: coordinates, value: int):
        self.coords = coords
        self.value = value

    def increment(self):
        self.value += 1

    def reset(self):
        self.value = 0

    @property
    def fired(self) -> bool:
        return self.value > 9

    def __repr__(self) -> str:
        return f"<row:{self.coords.row},col:{self.coords.col},value:{self.value}>"


MIN_IDX: int = 0
MAX_IDX: int = 9
octopi: Dict[coordinates, Octopus] = dict()
output: List[Tuple[Tuple[int, ...], ...]] = []
with open("input.txt", mode="rt") as inputfile:
    for row_idx, line in enumerate(inputfile):
        row: List[Octopus] = []
        for col_idx, value in enumerate(line.strip()):
            coords = coordinates(row=row_idx, col=col_idx)
            octopus = Octopus(coords, int(value))
            octopi[coords] = octopus


def get_frame(coords: coordinates) -> Tuple[Optional[Octopus], ...]:
    # if 4 represents coords, then the surrounding is array with indices corresponding
    # to the surroudning points of coords. None indicates no valid point available
    # (like when coords lie on the edges of the source array)
    # 0  1  2 ---------------------------- TOP ROW
    # 3 (4) 5 ----------------------------------------------- MIDDLE ROW
    # 6  7  8 --------------------------------------------------------------------------- BOTTOM ROW
    #                                      [0   , 1   , 2   , 3   , 4             , 5   , 6   , 7   , 8   ]
    surrounding: List[Optional[Octopus]] = [None, None, None, None, octopi[coords], None, None, None, None]
    if coords.row > MIN_IDX:
        surrounding[1] = octopi[coordinates(row=coords.row - 1, col=coords.col)]
        if coords.col > MIN_IDX:
            surrounding[0] = octopi[coordinates(row=coords.row - 1, col=coords.col - 1)]
        if coords.col < MAX_IDX:
            surrounding[2] = octopi[coordinates(row=coords.row - 1, col=coords.col + 1)]

    if coords.col > MIN_IDX:
        surrounding[3] = octopi[coordinates(row=coords.row, col=coords.col - 1)]

    if coords.col < MAX_IDX:
        surrounding[5] = octopi[coordinates(row=coords.row, col=coords.col + 1)]

    if coords.row < MAX_IDX:
        surrounding[7] = octopi[coordinates(row=coords.row + 1, col=coords.col)]
        if coords.col > MIN_IDX:
            surrounding[6] = octopi[coordinates(row=coords.row + 1, col=coords.col - 1)]
        if coords.col < MAX_IDX:
            surrounding[8] = octopi[coordinates(row=coords.row + 1, col=coords.col + 1)]

    return tuple(surrounding)


def do_step():
    # all values are incremented by one
    for o in octopi.values():
        o.increment()

    # evaluate fired positions
    fired: List[Octopus] = [o for o in octopi.values() if o.fired]
    while len(fired) > 0:
        for o in fired:
            # anything that is fired gets reset to zero
            o.reset()

            # get all neighboring values (including diagonal values)
            frame: Tuple[Optional[Octopus], ...] = get_frame(o.coords)

            # for each neighboring value
            for idx, o_sub in enumerate(frame):
                # idx 4 is original fired position and shouldnt be evaluated further/incremented
                if idx == 4:
                    continue

                # None so that we dont try to increment non-existent positions
                # value > 0 so that any position only fires once per step
                if o_sub is not None and o_sub.value > 0:
                    o_sub.increment()

        # keep going with newly fired positions
        fired = [o for o in octopi.values() if o.fired]


def print_state(state: Tuple[Tuple[int, ...], ...]):
    output: str = ""
    for r in state:
        rowstr: str = ""
        for v in r:
            rowstr += f"{'*' if v == 0 else str(v)} "
        output += f"{rowstr}".strip()
        output += "\n"

    return output


def record_state(size: int = 10):
    state: List[Tuple[int, ...]] = []
    for r in range(size):
        rlist: List[int] = []
        for c in range(size):
            rlist.append(octopi[coordinates(row=r, col=c)].value)
        state.append(tuple(rlist))
    output.append(tuple(state))


iteration: int = 0
record_state()
while True:
    iteration += 1
    do_step()
    fired_count = len([o for o in octopi.values() if o.value == 0])
    record_state()
    if fired_count == len(octopi):
        break

print(iteration)
print(print_state(output[len(output) - 1]))

with open("result.txt", mode="wt") as result:
    result.write(f"iteration all fired at once: {iteration}\n")

with open("output.txt", mode="wt") as outfile:
    for idx, state in enumerate(output):
        if idx == 0:
            outfile.write("initial state\n")
        else:
            outfile.write(f"iteration [{idx:> 4d}]\n")
        outfile.write(print_state(state))
        outfile.write("\n")
