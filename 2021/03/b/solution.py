import json
from typing import Any, List, Literal, Union

bits: List[Any] = []
with open("input.txt", mode="rt") as input:
    for idx, line in enumerate(input):
        _values = [int(i) for i in line.strip()]
        bits.append({"idx": idx, "value": _values})

steps: List[Any] = []


def filter_list(position: int, target_list: List[Any], favor: Union[Literal["most"], Literal["least"]]):
    ones = 0
    for b in target_list:
        ones += b["value"][position]

    zeroes = len(target_list) - ones

    search_key = 0
    match favor:
        # one ties for "most", prefer the `1` value
        case "most":
            if ones >= zeroes:
                search_key = 1
        # one ties for "least", prefer the `0` value
        case "least":
            if zeroes > ones:
                search_key = 1

    steps.append({"item_count": len(target_list), "favor": favor, "ones": ones, "zeroes": zeroes, "search_key": search_key})

    output = list(filter(lambda item: item["value"][position] == search_key, target_list))

    # with open(f"{favor}_step_{position:02d}.txt", mode="wt") as stepfile:
    #     stepfile.writelines(["".join([str(i) for i in v["value"]]) + "\n" for v in output])

    return output


oxygen_list: List[Any] = list(bits)
co2_list: List[Any] = list(bits)
for i in range(len(bits[0]["value"])):
    if len(oxygen_list) > 1:
        oxygen_list = filter_list(i, oxygen_list, "most")

    if len(co2_list) > 1:
        co2_list = filter_list(i, co2_list, "least")

oxygen: int = int("".join([str(i) for i in oxygen_list[0]["value"]]), base=2)
co2: int = int("".join([str(i) for i in co2_list[0]["value"]]), base=2)

print(oxygen_list, oxygen)
print(co2_list, co2)
print(oxygen * co2)

with open("result.txt", mode="wt") as result:
    result.writelines([
        f"oxygen rating: {oxygen}\n",
        f"co2 rating: {co2}\n",
        f"life support rating: {oxygen * co2}\n"
    ])

with open("output.json", mode="wt") as outfile:
    _o = sorted(sorted(steps, key=lambda c: c["item_count"], reverse=True), key=lambda f: f["favor"])
    outfile.write('[\n')
    for idx, item in enumerate(_o):
        outfile.write("    " + json.dumps(item))
        if idx != len(_o) - 1:
            outfile.write(",")
        outfile.write("\n")
    outfile.write(']\n')
    # outfile.write(json.dumps(sorted(sorted(steps, key=lambda c: c["item_count"], reverse=True), key=lambda f: f["favor"]), indent=4))
