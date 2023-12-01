import re


def parse_input(filename: str = "input.txt") -> str:
    rv: str = ""
    with open(filename, mode="rt") as inputfile:
        rv = inputfile.read().strip()

    return rv


re_tokens = re.compile(r"((\d)\2+)|(\d)")
input = parse_input()
working_input = input
for _ in range(50):
    tokens = re_tokens.findall(working_input)
    tokens = [t[0] if t[0] != "" else t[2] for t in tokens]
    rv: str = ""
    for t in tokens:
        rv += str(len(t)) + t[0]

    working_input = rv
    print(len(working_input))

with open("result.txt", mode="wt") as result:
    result.write(str(len(working_input)))

with open("output.txt", mode="wt") as outfile:
    working_input = input
    for _ in range(50):
        tokens = re_tokens.findall(working_input)
        tokens = [t[0] if t[0] != "" else t[2] for t in tokens]
        rv = ""
        for t in tokens:
            rv += str(len(t)) + t[0]

        working_input = rv
        outfile.write(f"{len(working_input): 9d}")
        outfile.write(" -> <full output elided>...\n")
