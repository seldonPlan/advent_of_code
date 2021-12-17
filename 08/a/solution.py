from typing import Dict, List, Tuple, Union

lines: List[Tuple[Tuple[str, ...], ...]] = []
with open("input.txt", mode="rt") as input:
    for line in input:
        lines.append(
            (
                tuple(line.split("|")[0].split()),
                tuple(line.split("|")[1].split()),
            )
        )

len_to_digit: Dict[int, Union[int, List[int]]] = {2: 1, 3: 7, 4: 4, 5: [2, 3, 5], 6: [0, 6, 9], 7: 8}

easy_nums: int = 0
for row in lines:
    for o in row[1]:
        if len(o) in [2, 3, 4, 7]:
            easy_nums += 1

print(easy_nums)

with open("result.txt", mode="wt") as result:
    result.write(str(easy_nums))

with open("output.txt", mode="wt") as outfile:
    for row in lines:
        for o in row[1]:
            outfile.write(f"{o:>8s} |")
        outfile.write("\n")

        for o in row[1]:
            if len(o) in [2, 3, 4, 7]:
                outfile.write(f"{len_to_digit[len(o)]:> 8d} |")
            else:
                outfile.write("         |")
        outfile.write(f"\n{'-' * 40}\n")
