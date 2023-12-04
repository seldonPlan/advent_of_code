import re
from html.parser import HTMLParser
from pathlib import Path
from typing import TypedDict

import requests
from markdownify import markdownify

CHALLENGE_YEAR = 2021
CHALLENGE_DAY = 1
CHALLENGE_PART = "a"

session: str | None = None
meta_path: Path = Path(__file__).parent.parent.joinpath("meta")


class ArticlePos(TypedDict):
    start: tuple[int, int]
    starttag: str
    end: tuple[int, int] | None


class ProblemParts(TypedDict):
    a: str
    b: str | None


class CompletionStatus(TypedDict):
    challenge_day: str
    completed: list[str]


class ArticleParser(HTMLParser):
    articles: list[ArticlePos] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "article":
            self.articles.append({"start": self.getpos(), "starttag": str(self.get_starttag_text())})
            # print("ARTICLE_START", self.getpos())

        return super().handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "article":
            self.articles[-1]["end"] = self.getpos()
            # print("ARTICLE_END", self.getpos())

        return super().handle_endtag(tag)


class CompletionCalendarParser(HTMLParser):
    completions: list[CompletionStatus] = []
    _day_matcher = re.compile(r"^day(?P<challenge_day>\d+)$", re.IGNORECASE)

    def parse_status_from_class(self, day: str, *status: str) -> CompletionStatus:
        retval = self._day_matcher.match(day).groupdict()

        if len(status) == 0:
            retval["completed"] = []
            return retval

        if "complete" in status:
            retval["completed"] = ["a"]
            return retval

        if "verycomplete" in status:
            retval["completed"] = ["a", "b"]
            return retval

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        cal_classes = [x[1] for x in attrs if x[0] == "class" and x[1].startswith("calendar")]

        if tag == "a" and len(cal_classes) > 0:
            status_classes = [x.replace("calendar-", "") for x in " ".join(cal_classes).split(" ")]
            self.completions.append(self.parse_status_from_class(*status_classes))

        return super().handle_starttag(tag, attrs)


def set_session():
    global session

    session_path = meta_path.joinpath(".session")
    if not session_path.exists():
        return

    with open(session_path, "rt") as session_file:
        session = str(session_file.read()).strip()


def write_file(path: Path, content: str):
    with open(path, "wt") as file:
        file.write(content)


def fetch_input() -> str:
    s = requests.Session()
    r = s.get(f"https://adventofcode.com/{CHALLENGE_YEAR}/day/{CHALLENGE_DAY}/input", cookies={"session": session})
    return str(r.text)


def fetch_calendar_progress() -> None:
    s = requests.Session()
    c = CompletionCalendarParser()

    r = s.get(f"https://adventofcode.com/{CHALLENGE_YEAR}/", cookies={"session": session})
    c.feed(r.text)
    return c.completions


def fetch_problem_descriptions() -> ProblemParts:
    s = requests.Session()
    h = ArticleParser()
    markdowns: ProblemParts = {"a": "", "b": None}

    r = s.get(f"https://adventofcode.com/{CHALLENGE_YEAR}/day/{CHALLENGE_DAY}", cookies={"session": session})

    h.feed(r.text)
    lines = str(r.text).splitlines()

    for idx, pos in enumerate(h.articles):
        article_text = lines[pos["start"][0] - 1 : pos["end"][0]]
        article_text[0] = article_text[0][pos["start"][1] :]
        article_text[-1] = article_text[-1][pos["end"][1] :]

        markdowns["a" if idx == 0 else "b"] = markdownify("\n".join(article_text))

    return markdowns


def main():
    # grab the session value for adventofcode.com
    set_session()

    # collect markdown-converted problem descriptions for challenge
    problems = fetch_problem_descriptions()
    write_file(meta_path.joinpath("problem.a.md"), problems["a"])
    write_file(meta_path.joinpath("problem.b.md"), problems["b"])

    # collect input data for challenge
    input = fetch_input()
    write_file(meta_path.joinpath("input.txt"), input)

    # collect completion statuses
    completed_status = fetch_calendar_progress()
    write_file(
        meta_path.joinpath(f"{CHALLENGE_YEAR}.status.txt"),
        "\n".join([f"day: {int(a['challenge_day']):02} | completed: {a['completed']}" for a in completed_status]),
    )


if __name__ == "__main__":
    main()
