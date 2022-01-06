from io import StringIO
from typing import Any, Dict, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        hex_str = inputfile.read().strip()

    for i in range(0, (int(len(hex_str) / 16) * 16) + 17, 16):
        bin_str = ""
        chunk = hex_str[i : i + 16]
        for hex_value in chunk:
            bin_str += f"{int(hex_value, base=16):04b}"

        if len(chunk) > 0:
            rv.append(bin_str)

    return rv


def bin_to_int(bin_str: str) -> int:
    return int(bin_str, base=2)


LITERAL_TYPE_CODE: str = "100"
OPERATOR_LENGTH_TYPE: str = "0"
OPERATOR_COUNT_TYPE: str = "1"


def parse_literal(stream: StringIO) -> List[str]:
    rv: List[str] = []

    component: str = stream.read(5)
    rv.append(component)

    while component.startswith("1"):
        component = stream.read(5)
        rv.append(component)

    return rv


def parse_packet(stream: StringIO):
    rv: Dict[Any, Any] = {}
    starting_position: int = stream.tell()

    header_size: int = 0
    packet_size: int = 0

    version_bin: str = stream.read(3)
    type_bin: str = stream.read(3)

    rv["version"] = {"bin": version_bin, "value": bin_to_int(version_bin)}
    rv["type"] = {"bin": type_bin, "value": bin_to_int(type_bin)}

    if type_bin == LITERAL_TYPE_CODE:
        header_size = stream.tell() - starting_position

        literal_arr = parse_literal(stream)
        rv["literal"] = [{"bin": v, "continue": v[0] == "1", "value": bin_to_int(v[1:])} for v in literal_arr]

        packet_size = len(literal_arr) * 5
    else:
        operator_type: str = stream.read(1)
        rv["operator"] = {
            "type": {
                "bin": operator_type,
                "value": bin_to_int(operator_type),
                "type": "LENGTH" if operator_type == OPERATOR_LENGTH_TYPE else "COUNT",
            }
        }

        if operator_type == OPERATOR_COUNT_TYPE:
            # OPERATOR_COUNT_TYPE (11 bit value)
            length_bin: str = stream.read(11)
            header_size = stream.tell() - starting_position

            # need to recursively fetch the count of packets and sum their sizes
            current_position = stream.tell()

            for _i in range(bin_to_int(length_bin)):
                _rv, sub_header_size, sub_packet_size = parse_packet(stream)
                packet_size += sub_header_size + sub_packet_size

            # reset back to current position, since recursive ops move the stream position
            stream.seek(current_position)

        if operator_type == OPERATOR_LENGTH_TYPE:
            # OPERATOR_LENGTH_TYPE (15 bit value)
            length_bin = stream.read(15)
            header_size = stream.tell() - starting_position

            packet_size = bin_to_int(length_bin)

        rv["operator"]["length"] = {"bin": length_bin, "value": bin_to_int(length_bin)}

    rv["size"] = {"header": header_size, "packet": packet_size, "total": header_size + packet_size}

    return rv, header_size, packet_size


bin_str_array: List[str] = parse_input()
stream: StringIO = StringIO("".join(bin_str_array))

output: List[Any] = []
try:
    wrapper, header_size, packet_size = parse_packet(stream)
    total_size: int = header_size + packet_size
    output.append(wrapper)

    while stream.tell() < total_size:
        # ignore packet sizes (they are recorded in packet dict)
        packet, _a, _b = parse_packet(stream)
        output.append(packet)
finally:
    stream.close()

print(sum([v["version"]["value"] for v in output]))

with open("result.txt", mode="wt") as result:
    result.write("version values: ")
    result.write(repr([v["version"]["value"] for v in output]))
    result.write("\n")
    result.write(f"sum of all version values: {sum([v['version']['value'] for v in output])}")
    result.write("\n")

with open("output.txt", mode="wt") as outfile:
    for packet in output:
        outfile.write(repr(packet))
        outfile.write("\n")

with open("input_bin.txt", mode="wt") as input_bin_file:
    for chunk in bin_str_array:
        input_bin_file.write(chunk)
        input_bin_file.write("\n")
