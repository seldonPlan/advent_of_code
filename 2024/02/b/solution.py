from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append([int(a) for a in line.strip().split()])

    return rv


input = parse_input()


def process_entry(entry: list[int]):
    def get_direction(comparison):
        if comparison > 0:
            return "up"

        if comparison < 0:
            return "down"

        if comparison == 0:
            return "same"

    checklist = []
    for idx in range(1, len(entry)):
        left = entry[idx - 1]
        right = entry[idx]

        _direction_val = right - left
        _direction = get_direction(_direction_val)
        checklist.append(((left, right), _direction, abs(_direction_val) >= 1 and abs(_direction_val) <= 3))

    is_valid = checklist[0][2]
    valid_count = 0
    for idx in range(1, len(checklist)):
        is_valid = True
        is_valid &= checklist[idx][2]
        is_valid &= checklist[idx][1] == checklist[idx - 1][1] and checklist[idx][1] != "same"

        valid_count += 1 if is_valid else 0

    errors = len(checklist) - valid_count

    # valid on its own
    if errors == 0:
        ...

    # has only one error
    if errors == 1:
        ...

    # multiple errors
    ...


with open("output.txt", mode="wt") as outfile:
    outfile.write(str(""))

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(""))
