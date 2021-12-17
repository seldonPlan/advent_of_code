from typing import List, Literal, Union

bit_mask: List[str] = ["0" for v in range(12)]

bits: List[int] = []
with open("input.txt", mode="rt") as input:
    bits = [int(line.strip(), 2) for line in input]


def walk_bit_mask(position: int, working: List[int], favor: Union[Literal["most"], Literal["least"]]):
    ones_mask = list(bit_mask)
    ones_mask[position] = "1"
    bit_shift = len(ones_mask) - (position + 1)
    ones_compare = int("".join([bit for bit in ones_mask]), 2)

    ones = len(list(filter(lambda value: value >> bit_shift == ones_compare >> bit_shift, working)))
    zeroes = len(working) - ones

    print({"shift": bit_shift, "ones": ones, "zeroes": zeroes})

    match favor:
        # ties when "most", prefer the `1` value
        case "most":
            if ones >= zeroes:
                bit_mask[position] = "1"
        # ties when "least", prefer the `0` value
        case "least":
            if zeroes > ones:
                bit_mask[position] = "1"

    compare = int("".join([bit for bit in bit_mask]), 2)
    output = list(filter(lambda value: value >> bit_shift == compare >> bit_shift, working))
    print(len(output))
    return output


_v: List[int] = list(bits)
for position in range(len(bit_mask)):
    _v = walk_bit_mask(position, _v, 'most')
    if len(_v) == 1:
        break

print(bit_mask, int("".join([str(v) for v in bit_mask]), 2))
print(_v[0])

# with open("result.txt", mode="wt") as result:
#     result.write(str(""))

# with open("output.json", mode="wt") as outfile:
#     outfile.write(json.dumps({}))
