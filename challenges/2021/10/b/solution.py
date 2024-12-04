from queue import Empty, LifoQueue
from typing import Dict, List, Tuple

lines: List[str] = []
with open("input.txt", mode="rt") as inputfile:
    lines = [i.strip() for i in inputfile.readlines()]

matching: Dict[str, str] = {"{": "}", "[": "]", "<": ">", "(": ")"}
scoring: Dict[str, int] = {")": 1, "]": 2, "}": 3, ">": 4}
output: List[Tuple[int, str, int]] = []

for line_idx, line in enumerate(lines):
    q: LifoQueue[str] = LifoQueue()
    has_error: bool = False
    for _idx, c in enumerate(line):
        if c in matching.keys():
            q.put_nowait(c)
        else:
            r = q.get_nowait()
            if c != matching[r]:
                has_error = True
                break
    if has_error:
        continue

    score: int = 0
    remainder: str = ""
    while True:
        try:
            r = matching[q.get_nowait()]
            score = (score * 5) + scoring[r]
            remainder += r
        except Empty:
            break

    output.append((line_idx, remainder, score))

output = sorted(output, key=lambda v: v[2])

print("middle score:", output[int(len(output) / 2)])

with open("result.txt", mode="wt") as result:
    result.write(f"middle score: {output[int(len(output) / 2)]}\n")

with open("output.txt", mode="wt") as outfile:
    for ac in output:
        outfile.write(repr(ac))
        outfile.write("\n")
