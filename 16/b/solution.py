from io import StringIO
from typing import Any, Dict, List, Optional, Tuple


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


# | type ID   | bin | operation    | description
# +-----------+-----+--------------+------------------------------------------------------------
# | type ID 0 | 000 | SUM          | at least one value
# | type ID 1 | 001 | PRODUCT      | at least one value (single value returns value)
# | type ID 2 | 010 | MINIMUM      | at least one value
# | type ID 3 | 011 | MAXIMUM      | at least one value
# | type ID 5 | 101 | GREATER THAN | exactly two values, 1 if first GREATER THAN second else 0
# | type ID 6 | 110 | LESS THAN    | exactly two values, 1 if first LESS THAN second else 0
# | type ID 7 | 111 | EQUAL TO     | exactly two values, 1 if first EQUAL TO second else 0
# | type ID 4 | 100 | LITERAL      | decoded values are joined to make a single value


TYPE_CODES = {
    "000": "SUM",
    "001": "PROD",
    "010": "MIN",
    "011": "MAX",
    "101": "GT",
    "110": "LT",
    "111": "EQ",
    "100": "LITERAL",
}

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
    rv["header"] = {}
    rv["payload"] = {}
    rv["size"] = {}
    starting_position: int = stream.tell()

    header_size: int = 0
    packet_size: int = 0

    version_bin: str = stream.read(3)
    type_bin: str = stream.read(3)
    rv["header"]["version"] = {"bin": version_bin, "value": bin_to_int(version_bin)}
    rv["header"]["type"] = {"bin": type_bin, "value": bin_to_int(type_bin), "code": TYPE_CODES[type_bin]}
    if type_bin == LITERAL_TYPE_CODE:
        header_size = stream.tell() - starting_position

        literal_arr = parse_literal(stream)
        literal_components = [{"bin": v, "continue": v[0] == "1", "value": v[1:]} for v in literal_arr]
        rv["payload"] = {
            "components": literal_components,
            "bin": "".join([str(v["value"]) for v in literal_components]),
            "value": bin_to_int("".join([str(v["value"]) for v in literal_components])),
        }

        packet_size = len(literal_arr) * 5
    else:
        operator_type: str = stream.read(1)
        rv["payload"] = {
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

        rv["payload"]["length"] = {"bin": length_bin, "value": bin_to_int(length_bin)}

    rv["size"] = {"header": header_size, "packet": packet_size, "total": header_size + packet_size}

    return rv, header_size, packet_size


def parse_op(op: Any, opstream: StringIO, size_target: Optional[int] = None):
    current_position = opstream.tell()
    if current_position > 0:
        # seek back one char and read
        opstream.seek(current_position - 1)
        check_value = opstream.read(1)
    else:
        check_value = ""

    match op["header"]["type"]["code"]:
        case "LITERAL":
            if check_value == ")":
                opstream.seek(current_position - 1)
                opstream.write(f"{op['payload']['value']},)")
            else:
                opstream.write(f"{op['payload']['value']},")

        case _:
            if check_value == ")":
                opstream.seek(current_position - 1)
                opstream.write(f"{op['header']['type']['code']}())")
            else:
                opstream.write(f"{op['header']['type']['code']}()")

    print(opstream.getvalue())


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

ops: List[Any] = []
for op in output:
    match op["header"]["type"]["code"]:
        case "LITERAL":
            ops.append(
                (
                    op["header"]["type"]["code"],
                    op['payload']['value'],
                    op["size"]["header"],
                    op["size"]["packet"],
                    op["size"]["total"]
                )
            )
        case _:
            ops.append(
                (
                    op["header"]["type"]["code"],
                    None,
                    op["size"]["header"],
                    op["size"]["packet"],
                    op["size"]["total"]
                )
            )

    print(ops[-1:][0])

ops = sorted(ops, reverse=True)


def process_command(operations: List[Tuple[Any, ...]], size: int = 0, target: Optional[int] = None):
    while True:
        try:
            op = operations.pop()
            if op[0] != "LITERAL":
                process_command(operations, 0, op[3])
        except IndexError:
            break

# command: str = ""
# while True:
#     try:
#         op = ops.pop()
#         if op[0] == "LITERAL":
#             ...
#         else:
#             ...

#     except IndexError:
#         break


with open("result.txt", mode="wt") as result:
    result.write("version values: ")
    result.write(repr([v["header"]["version"]["value"] for v in output]))
    result.write("\n")
    result.write(f"sum of all version values: {sum([v['header']['version']['value'] for v in output])}")
    result.write("\n")

with open("output.txt", mode="wt") as outfile:
    for packet in output:
        outfile.write(repr(packet))
        outfile.write("\n")

with open("input_bin.txt", mode="wt") as input_bin_file:
    for chunk in bin_str_array:
        input_bin_file.write(chunk)
        input_bin_file.write("\n")
