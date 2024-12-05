import json
from pathlib import Path
from typing import Any

# NOTE: there is a VERY important statement in the problem description for part (a) that is relevant here:
# """ The notation `X|Y` means that if both page number `X` and page number `Y` are to be produced as part of an update,
#     page number `X` *must* be printed at some point before page number `Y`.
# """
#
# BOTH X and Y must be in the candidate for the rule to apply. We CANNOT just take the rules altogether. each candidate
# has its own set of rules. A further clarification is made with an example:
# """ The first section specifies the *page ordering rules*, one per line. The first rule, `47|53`, means that if an
#     update includes both page number 47 and page number 53, then page number 47 *must* be printed at some point before
#     page number 53.
# """
#
# so for the example given, '47|53' would apply, while another rule involving 47 or 53 and some other (not present)
# number would NOT apply
#
# i'm leaving part (a) alone since this distinction apparently doesn't matter for that description, but it seems very
# relevant for part (b)


def parse_input(filename: str = "input.txt") -> list[Any]:
    rv: tuple[list[Any], list[Any]] = ([], [])
    with open(Path(__file__).parent.joinpath(filename), mode="rt") as inputfile:
        for line in inputfile:
            if "|" in line:
                rv[0].append([int(v) for v in line.strip().split("|")])

            if "," in line:
                rv[1].append([int(v) for v in line.strip().split(",")])

    return rv


def generate_ruleset(rules: set[tuple[int, ...]]):
    """convert a set of rule pairs (tuples) into a dict
    key is the target int that MUST COME AFTER all ints in the value (set)
    """
    parsed_rules = {}
    for rule in rules:
        if rule[1] not in parsed_rules:
            parsed_rules[rule[1]] = set()

        parsed_rules[rule[1]].add(rule[0])

    return parsed_rules


def check_candidate(candidate: list[int], ruleset: dict[int, set[int]]):
    """identify if a specific list violates the ruleset
    only identifies the first offending rule (by order in the candidate list)
    """
    for idx in range(len(candidate) - 1):
        tgt = candidate[idx]
        for val in candidate[idx + 1 :]:
            if val in ruleset.get(tgt, set()):
                return False, tgt, ruleset[tgt]

    return True, candidate[int(len(candidate) / 2)], None


raw_rules, orders = parse_input("input.txt")


def modify_candidate(candidate, tgt_value, rule):
    """swap the tgt_value to after the max index for all items in the rule"""
    _candidate = [*candidate]
    _candidate.remove(tgt_value)
    _candidate.insert(max(_candidate.index(v) for v in rule) + 1, tgt_value)

    return _candidate


total = 0
with open("output.txt", mode="wt") as outfile:
    # iterate through each order
    for order in orders:
        # identify order specific ruleset to be applied
        rules = set()
        for rule in raw_rules:
            if all(rule_value in order for rule_value in rule):
                rules.add(tuple(rule))

        ruleset = generate_ruleset(rules)
        outfile.write(
            f"order {json.dumps(order)}, has the following rules defined: f{json.dumps(generate_ruleset(rules), default=lambda x: str(list(x)))}\n"
        )

        is_valid, tgt_value, rule_violated = check_candidate(order, ruleset)

        outfile.write(
            f"{is_valid} | {tgt_value} | {json.dumps(rule_violated, default=lambda x: str(list(x)))}, {json.dumps(ruleset, default=lambda x: str(list(x)))}\n"
        )

        # part (b) only cares about orders that fail their first validation
        modified = [*order]
        while not is_valid:
            # this will run repeatedly, modifying the array per the offending rule each iteration
            # it "should" eventually become valid, breaking out of the loop
            modified = modify_candidate(modified, tgt_value, rule_violated)
            is_valid, tgt_value, rule_violated = check_candidate(modified, ruleset)
            outfile.write(f"{json.dumps(modified)}\n")
            outfile.write(f"{is_valid} | {tgt_value} | {json.dumps(rule_violated, default=lambda x: str(list(x)))}\n")

            # keep track of running sum of the "middle index" value. this is our result
            if is_valid:
                total += tgt_value

        outfile.write("\n")


with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(total))
