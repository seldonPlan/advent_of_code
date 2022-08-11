from typing import List

# this is an exercise in brute-force vs optimized solutions
# brute-force: track each fish in the array, and have the array size grow
#              exponentially higher and higher. My machine couldnt handle much
#              past the 150th - 175th iteration
# optimized: keep track of only the overall counts of fish. then we only ever keep
#            an array of 9 numbers (0 - 8), and do math on each value. The
#            individual counts move in blocks to the next value, and the zero counts
#            get added to the 6 block, and become the next 8 block

counts: List[int] = [0 for i in range(9)]
day_by_day: List[List[int]] = []
with open("input.txt", mode="rt") as input:
    for age in [int(i) for i in input.read().strip().split(",")]:
        counts[age] += 1

day_by_day.append([i for i in counts])


def process_generation(fish: List[int]):
    zero_count: int = fish[0]
    next_gen: List[int] = [0 for i in range(9)]
    for i in range(8):
        next_gen[i] = fish[i + 1]
    next_gen[8] = zero_count
    next_gen[6] += zero_count

    return next_gen


for _i in range(256):
    counts = process_generation(counts)
    day_by_day.append([i for i in counts])

print(counts, sum(counts))


with open("result.txt", mode="wt") as result:
    result.write(f"after 256 days: {sum(counts)} fish")

with open("output.txt", mode="wt") as outfile:
    for idx, day in enumerate(day_by_day):
        if idx == 0:
            outfile.write("initial  ")
        else:
            outfile.write(f"day {idx:> 4d} ")
        outfile.write(f"[{sum(day):> 14d} ]: ")
        for value in day:
            outfile.write(f"{value:> 13d}")
        outfile.write("\n")
