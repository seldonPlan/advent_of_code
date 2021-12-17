from typing import List

days: List[List[int]] = []
with open("input.txt", mode="rt") as input:
    days.append([int(i) for i in input.read().strip().split(",")])


def process_day(day: List[int]):
    _d: List[int] = [i for i in day]
    _n: List[int] = []
    for idx, age in enumerate(_d):
        if age > 0:
            _d[idx] = age - 1
        else:
            _d[idx] = 6
            _n.append(8)
    _d.extend(_n)

    return _d


for i in range(0, 80):
    days.append(process_day(days[i]))


print(len(days), len(days[80]))

with open("result.txt", mode="wt") as result:
    result.write(f"after 80 days: {len(days[80])} fish")

with open("output.txt", mode="wt") as outfile:
    for idx, day in enumerate(days):
        outfile.write(f"day {idx + 1:> 3d}: ")
        outfile.write("".join([str(v) for v in day]))
        outfile.write("\n")
