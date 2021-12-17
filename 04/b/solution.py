from typing import Any, List, Tuple

# unclear from problem text if there can be more than one winner in a round
# "correct" answer shows this is False
only_one_winner_per_round: bool = False

lines: List[Any] = []
draw_numbers: List[Any] = []
boards: List[List[List[Any]]] = []
winners: List[Tuple[List[List[Any]], int]] = []
with open("input.txt", mode="rt") as input:
    blocks = input.read().split("\n\n")
    draw_numbers = [int(b) for b in blocks[0].split(",")]
    boards = [[[int(b), False] for b in board.split()] for board in blocks[1:]]

    print(len(draw_numbers), draw_numbers)


def check_board(board: List[List[Any]]):
    # one of these indices must be True for a winning board
    if not any([board[i][1] for i in [0, 1, 2, 3, 4, 5, 10, 15, 20]]):
        return False

    runs: List[List[int]] = []
    # horizontal
    runs.extend([[i + j for j in range(5)] for i in [0, 5, 10, 15, 20]])
    # vertical
    runs.extend([[j for j in range(i, 25, 5)] for i in range(5)])

    for run in runs:
        if all([board[r][1] for r in run]):
            return True

    return False


def update_board(draw: int, board: List[List[Any]]):
    for pos in board:
        if pos[0] == draw:
            pos[1] = True


def calc_sum(board: List[List[Any]]):
    return sum([b[0] for b in list(filter(lambda v: not v[1], board))])


for idx, draw in enumerate(draw_numbers):
    # print("calling", draw)
    for board in boards:
        update_board(draw, board)
        if check_board(board):
            winners.append((board, draw))
            if only_one_winner_per_round:
                break

    boards = [b for b in boards if b not in [w[0] for w in winners]]
    print(f"{idx: 3d}", f"{draw: 3d}", f"{len(boards): 3d}", f"{len(winners): 3d}")
    if len(boards) == 0:
        break

row: str = ""
for idx, value in enumerate(winners[-1][0]):
    if idx in range(0, 25, 5):
        row += "\n"
    row += f"{value[0]:02d}[{'*' if value[1] else ' '}]   "
print(row)

print()
print("sum of unmarked numbers:", calc_sum(winners[-1][0]))
print("winning number:", winners[-1][1])
print("result:", winners[-1][1] * calc_sum(winners[-1][0]))

with open("result.txt", mode="wt") as result:
    result.write(f"sum of unmarked numbers: {calc_sum(winners[-1][0])}\n")
    result.write(f"winning number: {winners[-1][1]}\n")
    result.write(f"result: {winners[-1][1] * calc_sum(winners[-1][0])}\n")

with open("output.txt", mode="wt") as outfile:
    for board in [b[0] for b in winners]:
        row = ""
        for idx, value in enumerate(board):
            if idx in range(0, 25, 5):
                row += "\n"
            row += f"{value[0]:02d}[{'*' if value[1] else ' '}]   "
        outfile.write(row)
        outfile.write("\n\n")
