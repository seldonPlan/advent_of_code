import json
from typing import Any, List

course: List[Any] = []
with open("input.txt", mode="rt") as input:
    for idx, line in enumerate(input):
        _values = line.strip().split()
        course.append({"idx": idx, "command": _values[0], "distance": int(_values[1])})

horizontal_pos: int = 0
vertical_pos: int = 0

result: List[str] = []
for action in course:
    report: str = f'executing command {action["command"]} {action["distance"]} from ({horizontal_pos}, {vertical_pos}):'

    match action['command']:
        case 'forward':
            horizontal_pos += action['distance']
        case 'up':
            vertical_pos -= action['distance']
        case 'down':
            vertical_pos += action['distance']

    result.append(f'{report} new position ({horizontal_pos}, {vertical_pos})')

print(horizontal_pos * vertical_pos)

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(horizontal_pos * vertical_pos))

with open("report.json", mode="wt") as outfile:
    outfile.write(json.dumps(result))
