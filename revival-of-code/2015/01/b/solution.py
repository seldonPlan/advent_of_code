def parse_input(filename: str = "input.txt") -> tuple[str, int, int, int]:
    rv: str = ""
    up: int = 0
    down: int = 0
    idx: int = 0
    with open(filename, mode="rt") as inputfile:
        while True:
            s = inputfile.read(1)
            idx += 1
            rv += s
            match s:
                case "(":
                    up += 1
                case ")":
                    down += 1
                case "":
                    break
            if up - down == -1:
                break

    return rv, up, down, idx


input, up, down, pos = parse_input()

print("up:", up)
print("down:", down)
print("up - down:", up - down)
print("pos:", pos)

with open("result.txt", mode="wt") as result:
    result.write(f"{pos}\n")

with open("output.txt", mode="wt") as outfile:
    outfile.write(f"number of up directions [(]: {up}\n")
    outfile.write(f"number of down direction [)]: {down}\n")
    outfile.write(f"up [{up}] - down [{down}] = final floor [{up - down}]")
    outfile.write(f"position for basement (-1) = [{pos}]")
