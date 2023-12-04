#!/usr/bin/env python3 -B

from pathlib import Path

# zero padded days, 01 through 24
valid_days: list[str] = [f"{i:02}" for i in list(range(1, 26))]

# parts a and b
valid_parts: list[str] = ["a", "b"]

# filename keys, the existence of the files implies completion of a challenge part
# extensions can vary (i.e. solution.sh vs solution.py, problem.txt vs problem.md, etc...)
valid_files: list[str] = ["input", "output", "problem", "result", "solution"]


def dir_is_empty(dir: Path) -> bool:
    retval = True

    for obj in dir.iterdir():
        if not obj.name.startswith("."):
            retval = False
            break

    return retval


def next_open_slot(challenge_root: Path) -> tuple[str, str, str] | None:
    # next open slot is the first challenge of the a new challenge root
    if not challenge_root.exists():
        return (challenge_root.name, "01", "a")

    challenge_days: list[str] = [p.name for p in list(challenge_root.iterdir()) if p.name in valid_days]

    # assumes we walk the valid_challenge days in index order
    for day in valid_days:
        if day not in challenge_days:
            # next open slot is a new day
            return (challenge_root.name, day, "a")

        # assumes challenge_root.joinpath(valid_challenge_day) exists now
        checkval = "".join(
            sorted([p.name for p in list(challenge_root.joinpath(day).iterdir()) if p.name in valid_parts])
        )

        if "" == checkval:
            # next open slot the first subchallenge for the day
            return (challenge_root.name, day, "a")

        if "a" == checkval:
            # next open slot is the next subchallenge
            return (challenge_root.name, day, "b")

    # sentinel value, all challenges are assumed to be populated
    return None


if __name__ == "__main__":
    print(next_open_slot(Path(__file__).parent.parent.joinpath("revival-of-code").joinpath("2015")))
    print(next_open_slot(Path(__file__).parent.parent.joinpath("2023")))
    print(next_open_slot(Path(__file__).parent.parent.joinpath("2021")))
