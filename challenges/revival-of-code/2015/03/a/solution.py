def parse_input(filename: str = "input.txt") -> dict[tuple[int, int], int]:
    visits: dict[tuple[int, int], int] = {(0, 0): 1}
    current: tuple[int, int] = (0, 0)
    with open(filename, mode="rt") as inputfile:
        while True:
            d = inputfile.read(1)
            if d == "":
                break

            house = parse_move(current, d)
            if house in visits:
                visits[house] += 1
            else:
                visits[house] = 1

            current = house

    return visits


def parse_move(start: tuple[int, int], direction: str) -> tuple[int, int]:
    match direction:
        case "^":
            return start[0], start[1] + 1
        case ">":
            return start[0] + 1, start[1]
        case "v":
            return start[0], start[1] - 1
        case "<":
            return start[0] - 1, start[1]

    raise Exception(f"unknown direction {direction}")


visits = parse_input()
print(len(visits))

with open("result.txt", mode="wt") as result:
    result.write(f"{len(visits)}")

with open("output.txt", mode="wt") as outfile:
    for v in visits:
        outfile.write(f"{v}: {visits[v]}\n")
