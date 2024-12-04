import json
from functools import reduce
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append([int(a) for a in line.strip().split()])

    return rv


input = parse_input()


def fn_reducer(accumulator, value):
    prior, direction, status = accumulator

    def get_direction(comparison):
        if comparison > 0:
            return "up"

        if comparison < 0:
            return "down"

        if comparison == 0:
            return "same"

    # seed first value
    if prior is None:
        return (value, 0, True)

    # make comparison
    current_status = True

    _direction_value = value - prior
    _direction = get_direction(_direction_value)

    if _direction != direction and direction != 0:
        _direction = "changes"
        current_status &= False

    if abs(_direction_value) < 1 or abs(_direction_value) > 3:
        current_status &= False

    return (value, _direction, status and current_status)


output_val = []
for entry in input:
    output_val.append((entry, reduce(fn_reducer, entry, (None, None, None))))

with open("output.txt", mode="wt", encoding="utf-8") as outfile:
    for entry in output_val:
        checkme = " "
        if entry[1][1] == "up" and not entry[1][2]:
            checkme = "🔺"

        if entry[1][1] == "down" and not entry[1][2]:
            checkme = "🔻"

        if entry[1][1] == "changes" and not entry[1][2]:
            checkme = "🗙"

        if entry[1][2]:
            checkme = "✅"

        outfile.write(f" {checkme}\t")
        outfile.write(json.dumps(entry[0]))
        outfile.write(" | ")
        outfile.write(f"direction [{entry[1][1]}], status [{entry[1][2]}]")
        outfile.write("\n")

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(len([entry for entry in output_val if entry[1][2]])))
