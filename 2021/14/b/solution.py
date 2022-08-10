import json
from collections import Counter
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
counts: Dict[Tuple[str, ...], int] = {}
output: List[Dict[str, int]] = []


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

output.append({"".join(k): v for k, v in counts.items()})

for _i in range(40):
    # a tmp dict is required here because we cant update the counts object until
    # a complete pass through all of its keys. The iteration zeroes counts for
    # each pair as its goes, so if one of the child pairs are updated and happen
    # to match a pair to be yet updated in counts, there will be an inconsistent
    # state
    tmp: Dict[Tuple[str, ...], int] = {}
    for pair, count in counts.items():
        # since we are interested in "transforming" pairs and all possible pairs are
        # accounted for in the rule set, we can safely exclude any zero counts from
        # our processing. NOTE: A pair that is zero'd in one iteration can appear in
        # future iterations (i.e. from one of the child pairs )
        if count == 0:
            continue

        # since all pairs are accounted for in the rules, all existing pairs will be
        # transformed into child pairs. All parent pairs have their counts reset to
        # zero.

        # decrement parent pair
        update_counts(counts, pair, count * -1)

        # Any parent pair always produces two child pairs, all parent pairs are
        # transformed in equal amounts, so each child pair has the same output count
        # as the parent pair

        # increment child pair
        update_counts(tmp, (pair[0], rules[pair]), count)
        update_counts(tmp, (rules[pair], pair[1]), count)

    for pair, count in tmp.items():
        update_counts(counts, pair, count)

    output.append({"".join(k): v for k, v in counts.items()})

letter_counter: Counter = Counter()
for k, v in counts.items():
    letter_counter.update({k[0]: v})
letter_counter.update(input[-1:])
print(max(letter_counter.values()) - min(letter_counter.values()))

with open("result.txt", mode="wt") as result:
    result.write(json.dumps(letter_counter, indent=4))
    result.write("\n")


with open("output.txt", mode="wt") as outfile:
    for idx, state in enumerate(output):
        outfile.write(f"{idx:>03d}:  ")
        outfile.write(json.dumps(state))
        outfile.write("\n")
