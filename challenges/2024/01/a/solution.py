from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append(line.strip())

    return rv


input = parse_input()

# convert from strings to numerical pairs
input = [[int(b) for b in a.split("   ")] for a in input]

# split pairs into separate lists, then sort
left_list = tuple(sorted([a[0] for a in input]))
right_list = tuple(sorted([a[1] for a in input]))


# calc sum
sum_result = 0
with open("output.txt", mode="wt") as outfile:
    outfile.write("left  - right = diff  ; abs( diff) =  dist ;     sum + dist =   total\n")
    outfile.write("----------------------;--------------------;-------------------------\n")
    for idx in range(len(left_list)):
        diff = left_list[idx] - right_list[idx]
        outfile.write(
            f"{left_list[idx]} - {right_list[idx]} = {diff: >5} ; abs({diff: ^5}) = {abs(diff): >5} ; {sum_result: >7} + {abs(diff): >4} = {sum_result + abs(diff): >7}\n"
        )
        sum_result += abs(diff)
    outfile.write("----------------------;--------------------;-------------------------\n")
    outfile.write(f"\nresult: {sum_result}\n")

with open("result.txt", mode="wt") as result:
    result.write(str(sum_result))
