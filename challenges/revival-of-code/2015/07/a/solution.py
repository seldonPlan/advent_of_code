import math
import re
from typing import Any, List

"""
my first inclination was to build a "bottom -> top" stack implementation starting
from the desired "a" result and building up function pointers from there until
nothing could be added anymore. This resulted in some sort of O(n!) abomination
that took far too long for my machine to handle

the current solution takes a "top -> bottom" approach and treats the input like
a logic puzzle. I iterate through the entire op set looking for keys that can be
solved given what is known. At the start there are two keys that have known
values. Each iteration expands what can be solved from the values before it,
until every value is known and solved
"""


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []

    with open(filename, mode="rt") as inputfile:

        for line in inputfile:
            op, out = line.strip().split(" -> ")
            rv.append((parse_op(op), out))

    return rv


def parse_op(op: str) -> tuple[tuple[int | str, ...], str]:
    g: tuple[str, ...] = ()
    checks = [
        re.compile(r"^([a-z]+|\d+)$"),
        re.compile(r"^(NOT) ([a-z]+|\d+)$"),
        re.compile(r"^([a-z]+|\d+) (OR|AND) ([a-z]+|\d+)$"),
        re.compile(r"^([a-z]+|\d+) ((?:L|R)SHIFT) (\d+)$"),
    ]

    for r in checks:
        m = r.match(op)
        if m is not None:
            g = m.groups()
            break

    if len(g) == 1:
        return (parse_token(g[0]),), "EQ"

    if len(g) == 2:
        return (parse_token(g[1]),), g[0]

    if len(g) == 3:
        return (parse_token(g[0]), parse_token(g[2])), g[1]

    raise Exception(f"unknown op [{op}]")


def parse_token(tok: str) -> int | str:
    try:
        return int(tok)
    except ValueError:
        return tok


def solve(op: str, /, *args) -> int:
    # make sure args contain int values and not references
    _args = tuple([a if isinstance(a, int) else op_map[a]["value"] for a in args])

    match op:
        case "EQ":
            return _args[0]

        case "NOT":
            try:
                # circumvent ValueError when input is 0
                if _args[0] == 0:
                    return 1

                # calculate significant bit value
                # https://www.geeksforgeeks.org/find-significant-set-bit-number/
                msb = 1 << int(math.log(_args[0], 2))

                # calculate bit mask value
                mask = msb | (msb - 1)

                # perform NOT
                # https://realpython.com/python-bitwise-operators/#bitwise-not
                return ~_args[0] & mask
            except ValueError as err:
                print("ERROR:", op, *_args)
                raise err

        case "OR":
            return _args[0] | _args[1]

        case "AND":
            return _args[0] & _args[1]

        case "LSHIFT":
            return _args[0] << _args[1]

        case "RSHIFT":
            return _args[0] >> _args[1]

    raise Exception(f"unknown op [{op}]")


input = parse_input()

# init op_map
op_map: dict[str, dict[str, Any]] = {}
for i in input:
    op_map[i[1]] = {"op": i[0][1], "args": i[0][0], "value": None}

# iterate op_map indefinitely until we run out of keys to solve
# hopefully this gets us to the end
log: list[list[Any]] = []
solved_keys: set[str] = set()
while True:
    solvable_keys: list[str] = []

    # build solvable key list
    # solvable keys: any keys with args pointing to other keys that have already been solved
    for k, v in op_map.items():
        # shortcut known solved keys
        if k in solved_keys:
            continue

        solvable: bool = True
        for arg in v["args"]:
            if type(arg) == str and arg not in solved_keys:
                # int args are "known values"
                # str args that point to already solved keys are "known values"
                solvable = False

        if solvable:
            solvable_keys.append(k)

    # hopefully this happens at the end and not the middle of the chain
    if len(solvable_keys) == 0:
        log.append(["no new keys can be solved, breaking loop..."])
        print(" ".join(log[len(log) - 1]))
        break

    log.append(["new keys to be solved:", str(solvable_keys)])
    print(" ".join(log[len(log) - 1]))

    for k in solvable_keys:
        op_map[k]["value"] = solve(op_map[k]["op"], *(op_map[k]["args"]))
        log.append([k, str(op_map[k])])
        solved_keys.add(k)

print("a", op_map["a"]["value"])

with open("result.txt", mode="wt") as result:
    result.write(str(op_map["a"]["value"]))

with open("output.txt", mode="wt") as outfile:
    for entry in log:
        outfile.write(" ".join(entry))
        outfile.write("\n")
