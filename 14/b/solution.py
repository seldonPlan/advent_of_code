import json
from typing import Dict, List, Tuple


def parse_input(filename: str = "input.txt") -> Tuple[str, Dict[Tuple[str, ...], str]]:
    polymer: str = ""
    rules: Dict[Tuple[str, ...], str] = {}

    with open(filename, mode="rt") as inputfile:
        chunks = inputfile.read().split("\n\n")
        polymer = chunks[0]
        for rule_str in chunks[1].strip().split("\n"):
            rule_split = rule_str.split(" -> ")
            rules[tuple(list(rule_split[0]))] = rule_split[1]

    return polymer, rules


input, rules = parse_input()
log: List[str] = [input]


def process_step(input: str):
    pairs: List[Tuple[str, ...]] = []
    for i in range(1, len(input)):
        pairs.append((input[i - 1], input[i]))

    next: List[Tuple[str, ...]] = []
    for pair in pairs:
        if pair in rules:
            next.append((pair[0], rules[pair], pair[1]))
        else:
            next.append(pair)

    rv: str = next[0][0]
    for n in next:
        rv += "".join(n[1:])

    return rv


for i in range(40):
    print("iter", i)
    input = process_step(input)
    # log.append(input)

char_counts: Dict[str, int] = {}
for c in input:
    if c in char_counts:
        char_counts[c] += 1
    else:
        char_counts[c] = 1

sorted_result = sorted(tuple(char_counts.items()), key=lambda t: t[1], reverse=True)
print(sorted_result[0][1] - sorted_result[len(sorted_result) - 1][1])

with open("result.txt", mode="wt") as result:
    result.write("final counts:\n")
    result.write(json.dumps(char_counts, indent=4))
    result.write("\n\n")
    result.write(f"highest element: {repr(sorted_result[0])}\n")
    result.write(f"lowest element: {repr(sorted_result[len(sorted_result) - 1])}\n")
    result.write(f"difference: {sorted_result[0][1] - sorted_result[len(sorted_result) - 1][1]}\n")

with open("output.txt", mode="wt") as outfile:
    outfile.write("")
