from typing import Any, Dict, List


def gen_seven_segment_structure():
    return {
        "input": None,
        "output": None,
        "combined": [],
        "positions": {
            "bottom_left": {"potential": set(), "known": None},
            "top_left": {"potential": set(), "known": None},
            "top": {"potential": set(), "known": None},
            "top_right": {"potential": set(), "known": None},
            "bottom_right": {"potential": set(), "known": None},
            "bottom": {"potential": set(), "known": None},
            "middle": {"potential": set(), "known": None},
        },
    }


lines: List[Dict[Any, Any]] = []
with open("input.txt", mode="rt") as inputfile:
    for _l in inputfile:
        _d = gen_seven_segment_structure()
        _d["input"] = tuple(_l.split("|")[0].split())
        _d["output"] = tuple(_l.split("|")[1].split())
        _d["combined"].extend(_d["input"])
        _d["combined"].extend(_d["output"])
        lines.append(_d)


def rule_alpha(data):
    """
    ones should be processed first
      - len(word) == 2 for ones, and only ones
      - "letter" goes to "potential" of "top_right" and "bottom_right"
      - specific assignment cannot be made yet
    """

    for word in [w for w in data["combined"] if len(w) == 2]:
        for letter in word:
            data["positions"]["top_right"]["potential"].add(letter)
            data["positions"]["bottom_right"]["potential"].add(letter)


def rule_bravo(data):
    """
    sevens can be processed after ones
      - len(word) == 3 for sevens, and only sevens
      - interested in "letter" that is NOT in "potential" of "top_right" and "bottom_right"
      - able to determine specific assignment for "top"
    """

    for word in [w for w in data["combined"] if len(w) == 3]:
        for letter in word:
            if letter not in data["positions"]["top_right"]["potential"]:
                data["positions"]["top"]["potential"].add(letter)
                data["positions"]["top"]["known"] = letter


def rule_charlie(data):
    """
    fours can be processed after ones
      - len(word) == 4 for fours, and only fours
      - interested in "letter" that is NOT in "potential" of "top_right" and "bottom_right"
      - remaining "letter"s are in "potential" of "top_left" and "middle"
    """

    for word in [w for w in data["combined"] if len(w) == 4]:
        for letter in word:
            if letter not in data["positions"]["top_right"]["potential"]:
                data["positions"]["top_left"]["potential"].add(letter)
                data["positions"]["middle"]["potential"].add(letter)


def rule_delta(data):
    """
    sixes can be processed after sevens and fours
      - len(word) == 6 for sixes, zeroes, and nines
      - sixes should have one, but NOT both of "potential" for "top_right"
      - zeroes and nines will ALWAYS have both of "potential" for "top_right"
      - can add "potential" for "bottom_left" and "bottom"
      - able to determine specific assignment for "top_right"
      - able to determine specific assignment for "bottom_right"
    """
    all_except: List[str] = []
    all_except.extend(list(data["positions"]["top_right"]["potential"]))
    all_except.extend(list(data["positions"]["top_left"]["potential"]))
    all_except.extend(list(data["positions"]["top"]["potential"]))

    for word in [w for w in data["combined"] if len(w) == 6]:
        candidates = list(data["positions"]["top_right"]["potential"])
        counts = {candidates[0]: 0, candidates[1]: 0}
        for letter in word:
            if letter in candidates:
                counts[letter] += 1

        if counts[candidates[0]] == counts[candidates[1]]:
            # not a six, keep going
            continue

        # found the six
        if counts[candidates[0]] == 0:
            data["positions"]["top_right"]["potential"].add(candidates[0])
            data["positions"]["top_right"]["known"] = candidates[0]
            data["positions"]["bottom_right"]["potential"].add(candidates[1])
            data["positions"]["bottom_right"]["known"] = candidates[1]
        else:
            data["positions"]["top_right"]["potential"].add(candidates[1])
            data["positions"]["top_right"]["known"] = candidates[1]
            data["positions"]["bottom_right"]["potential"].add(candidates[0])
            data["positions"]["bottom_right"]["known"] = candidates[0]

        for letter in word:
            if letter not in all_except:
                data["positions"]["bottom_left"]["potential"].add(letter)
                data["positions"]["bottom"]["potential"].add(letter)


def rule_echo(data):
    """
    zeroes can be processed after fours
      - len(word) == 6 for sixes, zeroes, and nines
      - zeroes should have one, but NOT both of "potential" for "top_left"
      - sixes and nines will ALWAYS have both of "potential" for "top_left"
      - able to determine specific assignment for "top_left"
      - able to determine specific assignment for "middle"
    """

    for word in [w for w in data["combined"] if len(w) == 6]:
        candidates = list(data["positions"]["top_left"]["potential"])
        counts = {candidates[0]: 0, candidates[1]: 0}
        for letter in word:
            if letter in candidates:
                counts[letter] += 1

        if counts[candidates[0]] == counts[candidates[1]]:
            # not a zero, keep going
            continue

        # found the zero
        if counts[candidates[0]] == 0:
            data["positions"]["middle"]["potential"].add(candidates[0])
            data["positions"]["middle"]["known"] = candidates[0]
            data["positions"]["top_left"]["potential"].add(candidates[1])
            data["positions"]["top_left"]["known"] = candidates[1]
        else:
            data["positions"]["middle"]["potential"].add(candidates[1])
            data["positions"]["middle"]["known"] = candidates[1]
            data["positions"]["top_left"]["potential"].add(candidates[0])
            data["positions"]["top_left"]["known"] = candidates[0]


def rule_foxtrot(data):
    """
    nines can be processed after sixes
      - len(word) == 6 for sixes, zeroes, and nines
      - nines should have one, but NOT both of "potential" for "bottom_left"
      - sixes and zeroes will ALWAYS have both of "potential" for "bottom_left"
      - able to determine specific assignment for "bottom_left"
      - able to determine specific assignment for "bottom"
    """

    for word in [w for w in data["combined"] if len(w) == 6]:
        candidates = list(data["positions"]["bottom_left"]["potential"])
        counts = {candidates[0]: 0, candidates[1]: 0}
        for letter in word:
            if letter in candidates:
                counts[letter] += 1

        if counts[candidates[0]] == counts[candidates[1]]:
            # not a zero, keep going
            continue

        # found the zero
        if counts[candidates[0]] == 0:
            data["positions"]["bottom_left"]["potential"].add(candidates[0])
            data["positions"]["bottom_left"]["known"] = candidates[0]
            data["positions"]["bottom"]["potential"].add(candidates[1])
            data["positions"]["bottom"]["known"] = candidates[1]
        else:
            data["positions"]["bottom_left"]["potential"].add(candidates[1])
            data["positions"]["bottom_left"]["known"] = candidates[1]
            data["positions"]["bottom"]["potential"].add(candidates[0])
            data["positions"]["bottom"]["known"] = candidates[0]


def decode_positions(data):
    _p = data["positions"]
    # fmt: off
    _k = {
        "0": set(list([_p["top"]["known"], _p["top_right"]["known"], _p["top_left"]["known"], _p["bottom_right"]["known"], _p["bottom_left"]["known"], _p["bottom"]["known"]])),  # noqa: E501
        "1": set(list([_p["top_right"]["known"], _p["bottom_right"]["known"]])),  # noqa: E501
        "2": set(list([_p["top"]["known"], _p["top_right"]["known"], _p["middle"]["known"], _p["bottom_left"]["known"], _p["bottom"]["known"]])),  # noqa: E501
        "3": set(list([_p["top"]["known"], _p["top_right"]["known"], _p["middle"]["known"], _p["bottom_right"]["known"], _p["bottom"]["known"]])),  # noqa: E501
        "4": set(list([_p["top_left"]["known"], _p["top_right"]["known"], _p["middle"]["known"], _p["bottom_right"]["known"]])),  # noqa: E501
        "5": set(list([_p["top"]["known"], _p["top_left"]["known"], _p["middle"]["known"], _p["bottom_right"]["known"], _p["bottom"]["known"]])),  # noqa: E501
        "6": set(list([_p["top"]["known"], _p["top_left"]["known"], _p["middle"]["known"], _p["bottom_right"]["known"], _p["bottom_left"]["known"], _p["bottom"]["known"]])),  # noqa: E501
        "7": set(list([_p["top"]["known"], _p["top_right"]["known"], _p["bottom_right"]["known"]])),  # noqa: E501
        "8": set(list([_p["top"]["known"], _p["top_right"]["known"], _p["top_left"]["known"], _p["middle"]["known"], _p["bottom_right"]["known"], _p["bottom_left"]["known"], _p["bottom"]["known"]])),  # noqa: E501
        "9": set(list([_p["top"]["known"], _p["top_right"]["known"], _p["top_left"]["known"], _p["middle"]["known"], _p["bottom_right"]["known"], _p["bottom"]["known"]])),  # noqa: E501
    }
    # fmt: on
    data["decode"] = _k


def decode_value(decode, value):
    _value = set([v for v in value])
    for key in decode:
        if len(decode[key].difference(_value)) == 0 and len(_value) == len(decode[key]):
            # print(value, key)
            return key


output: List[int] = []
for line in lines:
    rule_alpha(line)
    rule_bravo(line)
    rule_charlie(line)
    rule_delta(line)
    rule_echo(line)
    rule_foxtrot(line)
    decode_positions(line)

    line["segment_output"] = []

    final_num: List[str] = []
    for value in line["output"]:
        _v = decode_value(line["decode"], value)
        line["segment_output"].append((value, _v))
        final_num.append(_v)

    line["display_value"] = "".join(final_num)
    output.append(int(line["display_value"]))
    print(line["segment_output"], line["display_value"])


with open("result.txt", mode="wt") as result:
    for line in lines:
        result.write(f"decoded values: {repr(line['segment_output']):<74s} | final display: {line['display_value']}\n")
    result.write(f"\nfinal output sum: {sum([int(i['display_value']) for i in lines])}\n")

with open("output.txt", mode="wt") as outfile:
    for line in lines:
        outfile.write(repr(line))
        outfile.write("\n")
