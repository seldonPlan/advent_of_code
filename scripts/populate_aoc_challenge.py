from pathlib import Path
from shutil import copy

CHALLENGE_YEAR = 2024
CHALLENGE_DAY = 2
CHALLENGE_PART = "b"

root_path: Path = Path(__file__).parent.parent
meta_path: Path = root_path.joinpath("meta")
tmpl_path: Path = root_path.joinpath(".template")
tgt_path: Path = Path(root_path / f"{CHALLENGE_YEAR}/{CHALLENGE_DAY:02}/{CHALLENGE_PART}")


def copy_file(src_file: Path, tgt_file: Path):
    if tgt_file.exists():
        print("file already exists:", tgt_file.relative_to(root_path))
    else:
        copy(src_file, tgt_file)


# copy problem
src_file = Path(meta_path / f"problem.{CHALLENGE_PART}.md")
tgt_file = Path(tgt_path / "problem.md")
copy_file(src_file, tgt_file)

# copy input
src_file = Path(meta_path / "input.txt")
tgt_file = Path(tgt_path / "input.txt")
copy_file(src_file, tgt_file)

# copy example solution
src_file = Path(tmpl_path / "solution.py")
tgt_file = Path(tgt_path / "solution.py")
copy_file(src_file, tgt_file)
