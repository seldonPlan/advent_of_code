#!/usr/bin/env python3 -B

import shutil
import sys
from pathlib import Path
from typing import Any, List


# assume script is running from child "scripts" dir
_AOC_ROOT: Path = Path(__file__).parent.parent

# root for template files to copy into each new step
_TEMPLATE_FILES: Path = _AOC_ROOT.joinpath("scripts/template/step")

# file containing a valid, existing prefix directory name
_PREFIX_FILE: Path = _AOC_ROOT.joinpath(".active_aoc")


# read contents of prefix_root for a recognized formatted directory structure
# append to directory structure from template
def main(prefix_root: Path):
    aoc_paths: List[Any] = []
    for dir in prefix_root.iterdir():
        try:
            # simple way to parse numeric directory name
            idx = int(dir.name)
            rv: Any = {"idx": idx, "name": dir.name, "path": dir, "sub": []}
            for subdir in dir.iterdir():
                if "a" == subdir.name or "b" == subdir.name:
                    rv["sub"].append(subdir.name)
            aoc_paths.append(rv)
        except ValueError:
            # non numeric directories wont be processed
            pass

    if len(aoc_paths) == 0:
        print("latest_work not found, creating first day...")
        mk_day(0, prefix_root)
        sys.exit(0)

    latest_work = sorted(aoc_paths, key=lambda v: v["name"])[-1]
    print("latest_work:",
        latest_work["path"]
            .joinpath('' if len(latest_work["sub"]) == 0 else sorted(latest_work["sub"])[-1])
            .relative_to(_AOC_ROOT)
    )

    # existence of "a" or "b" is enough, we dont need to care about their contents
    if "a" not in latest_work["sub"]:
        mk_step(latest_work["path"], "a")
    elif "b" not in latest_work["sub"]:
        mk_step(latest_work["path"], "b")
    else:
        mk_day(latest_work["idx"], prefix_root)


# append a numbered directory to active aoc prefix
def mk_day(idx: int, prefix_root: Path):
    newpath: Path = prefix_root.joinpath(f"{idx + 1:02d}")
    print("creating new day:", newpath.relative_to(_AOC_ROOT))
    newpath.mkdir(parents=False, exist_ok=False)
    mk_step(newpath, "a")


# append a step directory to path, copy template contents to new directory
def mk_step(path: Path, sub: str):
    newpath: Path = path.joinpath(sub)
    newpath.mkdir(parents=False, exist_ok=False)
    print("creating new step:", newpath.relative_to(_AOC_ROOT))
    shutil.copytree(_TEMPLATE_FILES, newpath, dirs_exist_ok=True)


# look for _PREFIX_FILE and create a valid path object from its contents
def get_prefix_root():
    if not _PREFIX_FILE.is_file():
        print(
f"""file '{_AOC_ROOT.name}/{_PREFIX_FILE.name}' not found
steps to fix:
    1. create text file with name '{_PREFIX_FILE.name}'
    2. populate file with the name of the current active prefix
    3. rerun this script"""
        )
        sys.exit(1)

    with open(_PREFIX_FILE, mode="rt") as prefix_file:
        active_prefix = prefix_file.read().strip()

    _PREFIX_ROOT: Path = _AOC_ROOT.joinpath(active_prefix).resolve()

    if not _PREFIX_ROOT.is_dir() or _AOC_ROOT.samefile(_PREFIX_ROOT):
        print(
f"""{_AOC_ROOT.name}/{_PREFIX_FILE.name}: '{active_prefix}' is not a valid prefix directory
steps to fix:
    1. populate '{_PREFIX_FILE.name}' with a valid, existing directory name located directly under '{_AOC_ROOT.name}/'
    2. rerun this script"""
        )
        sys.exit(1)

    return _PREFIX_ROOT


# kickoff script
main(get_prefix_root())

