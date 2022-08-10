from io import StringIO
from typing import Any, Dict, List, Optional


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


class OpNode(object):
    def __init__(self, type: str, line: int, header: int, packet: int, **k):
        self.type = type
        self.header = header
        self.packet = packet
        self.line = line
        self._literal: Optional[int] = None

        self.children: List[OpNode] = []

    def add(self, node: "OpNode"):
        self.children.append(node)

    @property
    def literal(self) -> Optional[int]:
        return self._literal

    @literal.setter
    def literal(self, value: int):
        self._literal = value

    @property
    def is_literal(self) -> bool:
        return self.type == "LITERAL"

    @property
    def total(self) -> int:
        return self.header + self.packet

    @property
    def sizeof_children(self) -> int:
        return sum([c.total for c in self.children])


def parse_nodes(ops: List[Any], idx: int = 0):
    wrapper = OpNode(ops[idx]["header"]["type"]["code"], idx + 1, ops[idx]["size"]["header"], ops[idx]["size"]["packet"])
    if wrapper.is_literal:
        wrapper.literal = int(ops[idx]["payload"]["value"])

    tracking = idx
    while wrapper.sizeof_children < wrapper.packet and not wrapper.is_literal:
        tracking += 1
        if tracking >= len(ops):
            break

        node, tracking = parse_nodes(ops, tracking)
        wrapper.add(node)

    # print(
    #     f"{tracking: 4d}",
    #     f"{idx: 4d}",
    #     f"{wrapper.type:>8s}",
    #     f"{wrapper.total: 4d}",
    #     f"{wrapper.packet: 4d}",
    #     f"  {str(wrapper.literal) if wrapper.literal is not None else '':<s}",
    # )
    return wrapper, tracking


root_node, _i = parse_nodes(output)
print(root_node.total, root_node.packet, root_node.sizeof_children)


def evaluate_nodes(root: OpNode, debug: bool = False):
    rv: Optional[int] = None
    match root.type:
        case "SUM":
            rv = sum([evaluate_nodes(c) for c in root.children])
            value = 0
            for child in root.children:
                value += evaluate_nodes(child)
            rv = value
            if debug:
                print("sum of", [evaluate_nodes(c, debug) for c in root.children], rv)
        case "PROD":
            value: int = 1
            for child in root.children:
                value *= evaluate_nodes(child)
            rv = value
            if debug:
                print("product of", [evaluate_nodes(c, debug) for c in root.children], rv)
        case "MIN":
            rv = min([evaluate_nodes(c) for c in root.children])
            if debug:
                print("min of", [evaluate_nodes(c, debug) for c in root.children], rv)
        case "MAX":
            rv = max([evaluate_nodes(c) for c in root.children])
            if debug:
                print("max of", [evaluate_nodes(c, debug) for c in root.children], rv)
        case "GT":
            rv = 1 if evaluate_nodes(root.children[0]) > evaluate_nodes(root.children[1]) else 0
            if debug:
                print("gt test", [evaluate_nodes(c, debug) for c in root.children], rv)
        case "LT":
            rv = 1 if evaluate_nodes(root.children[0]) < evaluate_nodes(root.children[1]) else 0
            if debug:
                print("lt test", [evaluate_nodes(c, debug) for c in root.children], rv)
        case "EQ":
            rv = 1 if evaluate_nodes(root.children[0]) == evaluate_nodes(root.children[1]) else 0
            if debug:
                print("eq test", [evaluate_nodes(c, debug) for c in root.children], rv)
        case "LITERAL":
            rv = root.literal

    return rv


badidea: Any = {}


def debug_nodes(root: OpNode, level: int = 0):
    sizes: List[Any] = []

    for child in root.children:
        clevel, cpacket, ctotal, csizes = debug_nodes(child, level + 1)
        if clevel in badidea:
            badidea[clevel].append((clevel, cpacket, ctotal, csizes))
        else:
            badidea[clevel] = [(clevel, cpacket, ctotal, csizes)]
        sizes.append((cpacket, ctotal))
        print(repr({"level": clevel, "packet": cpacket, "total": ctotal}))

    return level, root.packet, root.total, sizes


rlevel, rpacket, rtotal, rsizes = debug_nodes(root_node)
badidea[0] = [(rlevel, rpacket, rtotal, rsizes)]
print(repr(badidea))
print(evaluate_nodes(root_node, False))

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
