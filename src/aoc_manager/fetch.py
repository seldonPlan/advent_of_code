import re
from pathlib import Path
from typing import TypedDict
from bs4 import BeautifulSoup
import requests
from markdownify import markdownify


class CompletionStatus(TypedDict):
    challenge_day: str
    completed: list[str]


def get_session(session_file_path: Path):
    if not session_file_path.exists():
        session = "53616c7465645f5fd9f32c1bcb2a910a427fc38c3756e5acec95b86eb606c4887a1e6de471103c34f2d33f125d172387aa3eb08fd41d9e95ce0fde66e0372d25"

    else:
        with open(session_file_path, "rt") as session_file:
            session = str(session_file.read()).strip()

    return session


def write_file(path: Path, content: str):
    with open(path, "wt") as file:
        file.write(content)


def fetch_input(session: str, year: int, day: int) -> str:
    s = requests.Session()
    r = s.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies={"session": session})
    return str(r.text)


def fetch_calendar_progress(session: str, year: int) -> list[CompletionStatus]:
    s = requests.Session()

    r = s.get(f"https://adventofcode.com/{year}/", cookies={"session": session})

    soup = BeautifulSoup(r.content, "html.parser")
    class_groups = [t.attrs["class"] for t in list(soup.find_all("a", class_=re.compile(r"calendar-.*")))]
    for idx, classes in enumerate(class_groups):
        class_groups[idx] = [cls.replace("calendar-", "") for cls in classes]

    completions: list[CompletionStatus] = []
    for classes in class_groups:
        completion: CompletionStatus = re.match(r"^day(?P<challenge_day>\d+)$", classes[0]).groupdict()  # type: ignore [assignment, union-attr]

        if len(classes) == 1:
            completion["completed"] = []

        if "complete" in classes[1:]:
            completion["completed"] = ["a"]

        if "verycomplete" in classes[1:]:
            completion["completed"] = ["a", "b"]

        completions.append(completion)

    return completions


def fetch_problem_descriptions(session: str, year: int, day: int) -> dict[str, str | None]:
    s = requests.Session()
    markdowns = {"a": "", "b": None}

    r = s.get(f"https://adventofcode.com/{year}/day/{day}", cookies={"session": session})

    soup = BeautifulSoup(r.content, "html.parser")
    articles = list(soup.find_all("article", attrs={"class": "day-desc"}))

    for idx, article in enumerate(articles):
        markdowns["a" if idx == 0 else "b"] = markdownify(str(article))

    return markdowns


def main():
    CHALLENGE_YEAR = 2015
    CHALLENGE_DAY = 1
    CHALLENGE_PART = "a"

    meta_path: Path = Path(__file__).parent.parent.parent.joinpath("meta")

    # grab the session value for adventofcode.com from locally cached token
    session = get_session(meta_path.joinpath(".session"))

    # collect markdown-converted problem descriptions for challenge
    problems = fetch_problem_descriptions(session, CHALLENGE_YEAR, CHALLENGE_DAY)
    write_file(meta_path.joinpath("problem.a.md"), problems["a"])
    write_file(meta_path.joinpath("problem.b.md"), problems["b"])

    # collect input data for challenge
    input = fetch_input(session, CHALLENGE_YEAR, CHALLENGE_DAY)
    write_file(meta_path.joinpath("input.txt"), input)

    # collect completion statuses
    completed_status = fetch_calendar_progress(session, CHALLENGE_YEAR)
    write_file(
        meta_path.joinpath(f"{CHALLENGE_YEAR}.status.txt"),
        "\n".join([f"day: {int(a['challenge_day']):02} | completed: {a['completed']}" for a in completed_status]),
    )


if __name__ == "__main__":
    main()
