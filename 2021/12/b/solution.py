import string
from typing import Dict, List, Set, Tuple


class Node(object):
    def __init__(self, name: str):
        self.name: str = name
        self.type: str = ""
        if self.name in ["start", "end"]:
            self.type = self.name
        elif all([(i in string.ascii_uppercase) for i in self.name]):
            self.type = "big"
        else:
            self.type = "small"

        self._connections: Set[Node] = set()

    def add_connection(self, connection: "Node"):
        self._connections.add(connection)

    @property
    def is_small(self) -> bool:
        return self.type == "small"

    @property
    def is_big(self) -> bool:
        return self.type == "big"

    @property
    def is_end(self) -> bool:
        return self.type == "end"

    @property
    def connections(self) -> List[str]:
        return sorted([n.name for n in list(self._connections)])

    def __repr__(self) -> str:
        return f"Node<{self.name:>5s}, {self.type:<5s}, [{','.join(self.connections)}]>"

    def __hash__(self):
        return hash(str(self.name))

    def __eq__(self, other):
        return self.name == other.name


def parse_input(filename: str = "input.txt") -> Dict[str, Node]:
    node_set: Set[Node] = set()
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            n = line.strip().split("-")
            node_set.add(Node(n[0]))
            node_set.add(Node(n[1]))

            n0 = [i for i in list(node_set) if i.name == n[0]][0]
            n1 = [i for i in list(node_set) if i.name == n[1]][0]

            n0.add_connection(n1)
            if n1.name not in ["start", "end"] and n0.name not in ["start"]:
                n1.add_connection(n0)

    output: Dict[str, Node] = {}
    for node in node_set:
        output[node.name] = node

    return output


nodes = parse_input()
# for i in nodes:
#     print(nodes[i])

active_node: Node = nodes["start"]
output: List[Tuple[str, ...]] = []


def process(active_node: Node, current: Tuple[str, ...]):
    small_node_count: Dict[str, int] = {}
    for c in current:
        if nodes[c].is_small:
            if c in small_node_count:
                small_node_count[c] += 1
            else:
                small_node_count[c] = 1

    def valid_nodes(name: str):
        if nodes[name].is_end:
            return True

        if nodes[name].is_big:
            return True

        if nodes[name].is_small:
            if all([n < 2 for n in list(small_node_count.values())]):
                return True

            if name not in list(small_node_count.keys()):
                return True

        return False

    possibilities: List[str] = list(filter(valid_nodes, active_node.connections))

    if len(possibilities) == 0 or active_node.name == "end":
        yield current
        return

    for next in possibilities:
        for n in process(nodes[next], (*current, next)):
            yield n


output.extend(process(nodes["start"], ("start",)))
path_set: Set[Tuple[str, ...]] = set()
for o in [o for o in output if o[len(o) - 1] == "end"]:
    path_set.add(o)

print(len(path_set))

with open("result.txt", mode="wt") as result:
    result.write(f"total paths: {len([o for o in output if o[len(o) - 1] == 'end'])}")

with open("output.txt", mode="wt") as outfile:
    for o in output:
        outfile.write(repr(o))
        outfile.write("\n")
