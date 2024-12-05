from pathlib import Path
from typing import Any


def parse_input(filename: str = "input.txt") -> list[Any]:
    rv: tuple[list[Any], list[Any]] = ([], [])
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            if "|" in line:
                rv[0].append([int(v) for v in line.strip().split("|")])

            if "," in line:
                rv[1].append([int(v) for v in line.strip().split(",")])

    return rv


raw_rules, orders = parse_input("input.txt")

parsed_rules = {}
for rule in raw_rules:
    if rule[1] not in parsed_rules:
        parsed_rules[rule[1]] = set()

    parsed_rules[rule[1]].add(rule[0])


def check_candidate(candidate: list[int]):
    for idx in range(len(candidate) - 1):
        tgt = candidate[idx]
        for val in candidate[idx + 1 :]:
            if val in parsed_rules.get(tgt, set()):
                return False, tgt, parsed_rules[tgt]

    return True, candidate[int(len(candidate) / 2)], None


total = 0
with open("output.txt", mode="wt") as outfile:
    outfile.write("===== RULE DEFINITIONS =====\n")
    for key in sorted(parsed_rules.keys()):
        outfile.write(f"{key: >2} must come after [{', '.join([str(v) for v in parsed_rules[key]])}]\n")

    outfile.write("\n===== ORDERS =====\n")
    for order in sorted(orders):
        is_valid, tgt_value, _rule_violated = check_candidate(order)
        outfile.write(
            f"{len(order): >2} | [{', '.join([str(v) for v in order]): <90}] | {str(is_valid): >5} | {tgt_value: >2}"
        )

        if not is_valid:
            outfile.write(f" must come after [{', '.join([str(v) for v in _rule_violated])}]")

        if is_valid:
            outfile.write(" (middle of order list)")
            total += tgt_value

        outfile.write("\n")

    outfile.write("\n===== TOTAL =====\n")
    outfile.write(f"total sum of middle values of all valid orders: {total}")

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(total))
