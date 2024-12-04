from collections import deque
from typing import Any, List


def parse_input(filename: str = "input.txt") -> List[Any]:
    rv: List[Any] = []
    with open(filename, mode="rt") as inputfile:
        for line in inputfile:
            rv.append(line.strip())

    return rv


input = parse_input()

# convert from strings to numerical pairs
input = [[int(b) for b in a.split("   ")] for a in input]

# split pairs into separate lists, then sort
left_list = deque(sorted([a[0] for a in input]))
right_list = deque(sorted([a[1] for a in input]))


with open("output.txt", mode="wt") as outfile:
    for idx in range(len(left_list)):
        outfile.write(f"{left_list[idx]}   {right_list[idx]}\n")


# assume both lists are sorted, low to high
# lets look at each list like a series of numbers on a written on a long tape (this is represented by the deque data structure)
# lets assume that we only pull the tape upwards from the top end, so we will only cycle through the numbers from top to bottom (this is represented by only using popleft to get the next value)
# per the problem definition we are interested in how many times a value on the left list appears on the right list

# seed our iteration with the first value from each list
# the cursor is the number that we are currently "pointing" at from each list
cursor_left = left_list.popleft()
cursor_right = right_list.popleft()

# we need to keep track of a few values from outside the iteration
# `running_sum` will eventually be our final result, and `check_count` will help keep track of runs of the same number
running_sum = 0
check_count = 0
SENTINEL_DUMMY_VALUE = -9999999999

# each iteration will compare the values of our cursors. sorting the lists helps here, since we know the next value in any list will always be equal or greater
# our goal is to "pull the tape" from the left or right lists to find cursor values that are as close as possible to each other
# once we find values that are equal, we keep track of how many times they are equal, and use that to calculate the "similarity score" (from the problem description)
# for instance, if the left cursor is smaller than the right, then we should "pull the tape" on the left list to move to its next value to see if its any closer to the right

while True:
    # this our check_count condition, and is used to "flush" our current similarity score to the running_sum
    # if there is a run of the same value on the left side, we also move through each one, adding their scores as well
    if cursor_right != cursor_left and check_count > 0:
        curr_check = cursor_left
        while True:
            running_sum += cursor_left * check_count

            try:
                cursor_left = left_list.popleft()
            except IndexError:
                cursor_left = SENTINEL_DUMMY_VALUE

            if cursor_left != curr_check:
                break

        check_count = 0
        if cursor_left == SENTINEL_DUMMY_VALUE:
            break

    # if the RIGHT cursor is BIGGER, than we should move to the next biggest value on the LEFT side
    if cursor_right > cursor_left:
        try:
            cursor_left = left_list.popleft()
        except IndexError:
            break

        continue

    # when the cursors are equal, then increase our check count, and move to the next biggest value on the RIGHT side
    if cursor_right == cursor_left:
        check_count += 1
        try:
            cursor_right = right_list.popleft()
        except IndexError:
            # since its possible for this to happen at the very end of the right list, we should use a sentinel value
            # and move to the next iteration to ensure the running_sum is updated with the check_count
            cursor_right = SENTINEL_DUMMY_VALUE

        continue

    # if the LEFT cursor is BIGGER, than we should move to the next biggest value on the RIGHT side
    if cursor_right < cursor_left:
        try:
            cursor_right = right_list.popleft()
        except IndexError:
            break

        continue

    break

with open("result.txt", mode="wt") as resultfile:
    resultfile.write(str(running_sum))
