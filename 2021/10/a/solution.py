from queue import LifoQueue
from typing import Dict, List, Tuple

lines: List[str] = []
with open("input.txt", mode="rt") as inputfile:
    lines = [i.strip() for i in inputfile.readlines()]

matching: Dict[str, str] = {"{": "}", "[": "]", "<": ">", "(": ")"}
illegal: Dict[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}
syntax_errors: List[Tuple[str, str, str]] = []

illegal_sum: int = 0
for line_idx, line in enumerate(lines):
    q: LifoQueue[str] = LifoQueue()
    has_error: bool = False
    for c_idx, c in enumerate(line):
        if c in matching.keys():
            q.put_nowait(c)
        else:
            r = q.get_nowait()
            if c != matching[r]:
                has_error = True
                illegal_sum += illegal[c]
                se = (f"SYNTAX ERROR [{line_idx}] at [{c_idx}]:", f"expected {matching[r]} but found {c} instead", line)
                syntax_errors.append(se)

    # remaining_qsize = q.qsize()
    # remainder: str = ""
    # while True:
    #     try:
    #         remainder += q.get_nowait()
    #     except Empty:
    #         break
    # if not has_error:
    #     print(f"line [{line_idx}] has [{remaining_qsize}] elements remaining: {remainder}")

print(illegal_sum)

with open("result.txt", mode="wt") as result:
    result.write(f"syntax error score: {illegal_sum}")

with open("output.txt", mode="wt") as outfile:
    for se in syntax_errors:
        outfile.write(" ".join(se))
        outfile.write("\n")
