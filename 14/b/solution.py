from typing import Dict, Tuple


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
counts: Dict[Tuple[str, ...], int] = {}


def update_counts(d: Dict[Tuple[str, ...], int], key: Tuple[str, ...], count: int):
    try:
        d[key] += count
    except KeyError:
        d[key] = count


# init counts with all possible pairs, with value of zero
for pair, _s in rules.items():
    update_counts(counts, pair, 0)

# populate with counts of initial strings
for i, j in zip(input[:-1], input[1:]):
    update_counts(counts, (i, j), 1)

for _i in range(40):
    # a tmp dict is required here because we cant update the counts object until
    # a complete pass through all of its keys. The iteration zeroes counts for
    # each pair as its goes, so if one of the child pairs are updated and happen
    # to match a pair to be yet updated in counts, there will be an inconsistent
    # state
    tmp: Dict[Tuple[str, ...], int] = {}
    for pair, count in counts.items():
        if count == 0:
            continue

        # decrement parent pair
        update_counts(counts, pair, count * -1)

        # increment child pair
        update_counts(tmp, (pair[0], rules[pair]), count)
        update_counts(tmp, (rules[pair], pair[1]), count)

    for pair, count in tmp.items():
        update_counts(counts, pair, count)

    print({"".join(p): c for p, c in counts.items() if c > 0})
    print("-" * 80)
