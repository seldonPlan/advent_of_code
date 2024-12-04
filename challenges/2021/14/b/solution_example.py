from typing import Any

# credit to:
#  - https://gitlab.com/carlospereiraf/aoc/-/blob/main/2021/py/day-14.py
#  - https://www.reddit.com/r/adventofcode/comments/rfzq6f/2021_day_14_solutions/


def parse_input(filename: str = "input.txt"):
    with open(filename, mode="rt") as inputfile:
        seq = inputfile.readline().strip()
        next(inputfile)
        rules: Any = [line.strip().split(" -> ") for line in inputfile]
        rules = {rule: val for rule, val in rules}

    return seq, rules


def adjust_count(d, key, count):
    try:
        d[key] += count
    except KeyError:
        d[key] = count


def part_two(seq, rules, n):
    last_letter = seq[-1]

    # Store initial pair counts
    pairs = {}
    for l1, l2 in zip(seq[:-1], seq[1:]):
        adjust_count(pairs, l1 + l2, 1)

    for _i in range(n):
        pairs_temp = {}
        for pair, count in pairs.items():
            if count == 0:
                continue
            pairs[pair] -= count
            add = rules[pair]
            adjust_count(pairs_temp, pair[0] + add, count)
            adjust_count(pairs_temp, add + pair[1], count)

        for pair, count in pairs_temp.items():
            adjust_count(pairs, pair, count)

    # Count letters
    counts = {}
    for _j, (pair, count) in enumerate(pairs.items()):
        if count != 0:
            adjust_count(counts, pair[0], count)

    # Make sure last letter is counted
    counts[last_letter] += 1
    return max(counts.values()) - min(counts.values())


seq, rules = parse_input()
print(part_two(seq, rules, 40))
