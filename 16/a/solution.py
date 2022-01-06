from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        hex_str = inputfile.read().strip()

    for i in range(0, (int(len(hex_str) / 16) * 16) + 17, 16):
        bin_str = ""
        chunk = hex_str[i : i + 16]
        for hex_value in chunk:
            bin_str += f"{int(hex_value, base=16):04b}"

        if len(chunk) > 0:
            rv.append(bin_str)

    return rv


input = parse_input()

bin_str = "".join(input)
print(len(bin_str))
print(bin_str[0:22])


# with open("result.txt", mode="wt") as result:
#     result.write(str(""))

# with open("output.txt", mode="wt") as outfile:
#     outfile.write(str(""))
