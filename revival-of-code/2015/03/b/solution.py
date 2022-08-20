def parse_input(filename: str = "input.txt") -> dict[tuple[int, int], int]:
    visits: dict[tuple[int, int], int] = {(0, 0): 1}
    santa_current: tuple[int, int] = (0, 0)
    robo_current: tuple[int, int] = (0, 0)
    with open(filename, mode="rt") as inputfile:
        while True:
            d = inputfile.read(2)
            if d == "":
                break

            robo_house = parse_move(robo_current, d[0])
            santa_house = parse_move(santa_current, d[1])
            for house in [robo_house, santa_house]:
                if house in visits:
                    visits[house] += 1
                else:
                    visits[house] = 1

            robo_current = robo_house
            santa_current = santa_house

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
