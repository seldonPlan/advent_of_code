#!/usr/local/opt/python@3.10/bin/python3 -B

import shutil
from pathlib import Path
from typing import Any, List

_AOC_ROOT: Path = Path(__file__).parent.parent
_TEMPLATE_FILES: Path = _AOC_ROOT.joinpath("scripts/template/step")


def main():
    aoc_paths: List[Any] = []
    for dir in _AOC_ROOT.iterdir():
        try:
            # simple way to parse numeric directory name
            idx = int(dir.name)
            rv: Any = {"idx": idx, "name": dir.name, "path": dir, "sub": []}
            for subdir in dir.iterdir():
                if "a" == subdir.name or "b" == subdir.name:
                    rv["sub"].append(subdir.name)
            aoc_paths.append(rv)
        except ValueError:
            pass

    latest_work = sorted(aoc_paths, key=lambda v: v["name"])[-1]
    print("latest_work:", latest_work["path"].relative_to(_AOC_ROOT))
    if "a" not in latest_work["sub"]:
        mk_step(latest_work["path"], "a")
    elif "b" not in latest_work["sub"]:
        mk_step(latest_work["path"], "b")
    else:
        newpath: Path = _AOC_ROOT.joinpath(f"{latest_work['idx'] + 1:02d}")
        print("creating new day:", newpath.relative_to(_AOC_ROOT))
        newpath.mkdir(parents=False, exist_ok=False)
        mk_step(newpath, "a")


def mk_step(path: Path, sub: str):
    newpath: Path = path.joinpath(sub)
    newpath.mkdir(parents=False, exist_ok=False)

    print("creating new step:", newpath.relative_to(_AOC_ROOT))
    shutil.copytree(_TEMPLATE_FILES, newpath, dirs_exist_ok=True)


main()
