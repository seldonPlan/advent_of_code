from typing import Any, List, Tuple

lines: List[Any] = []
draw_numbers: List[Any] = []
boards: List[List[List[Any]]] = []
winner: Tuple[List[List[Any]], int] = ([], -1)
with open("input.txt", mode="rt") as input:
    blocks = input.read().split("\n\n")
    draw_numbers = [int(b) for b in blocks[0].split(",")]
    boards = [[[int(b), False] for b in board.split()] for board in blocks[1:]]

    print(len(draw_numbers), draw_numbers)
    # for board in boards:
    #     print(len(board), json.dumps(board))


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


for draw in draw_numbers:
    print("calling", draw)
    for board in boards:
        update_board(draw, board)
        if check_board(board):
            print("BINGO!")
            row: str = ""
            for idx, value in enumerate(board):
                if idx in range(0, 25, 5):
                    row += "\n"
                row += f"{value[0]:02d}[{'*' if value[1] else ' '}]   "
            print(row)
            winner = board, draw
            break

    # https://stackoverflow.com/a/3150107
    else:
        # continue when inner loop isnt broken
        continue

    # inner loop broken, break the outer loop
    break


print("sum of unmarked numbers:", calc_sum(winner[0]))
print("winning number:", winner[1])
print("result:", winner[1] * calc_sum(winner[0]))

with open("result.txt", mode="wt") as result:
    result.write(f"sum of unmarked numbers: {calc_sum(winner[0])}\n")
    result.write(f"winning number: {winner[1]}\n")
    result.write(f"result: {winner[1] * calc_sum(winner[0])}\n")

with open("output.txt", mode="wt") as outfile:
    for board in boards:
        row = ""
        for idx, value in enumerate(board):
            if idx in range(0, 25, 5):
                row += "\n"
            row += f"{value[0]:02d}[{'*' if value[1] else ' '}]   "
        outfile.write(row)
        outfile.write("\n\n")
