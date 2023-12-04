#!/usr/bin/env python3 -B

import os
import platform
import sqlite3
from pathlib import Path

# print("system params:", os.name, platform.system())
# print(__file__)

# location of profiles directory
# https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data#w_finding-your-profile-without-opening-firefox
profile_dirname = {
    "Windows": "%APPDATA%/Mozilla/Firefox/Profiles",
    "Darwin": "~/Library/Application Support/Firefox/Profiles",
    "Linux": "${HOME}/.mozilla/firefox",
}[platform.system()]

profiles = Path(os.path.expandvars(profile_dirname)).expanduser().resolve().absolute()


def find_cookies_file(profiles: Path) -> Path | None:
    # return the first matching cookies file we find
    for profile_dir in profiles.iterdir():
        if profile_dir.joinpath("cookies.sqlite").exists():
            return profile_dir.joinpath("cookies.sqlite")

    return None


def query_cookies_file(cookie_db: Path) -> str | None:
    con = sqlite3.connect(f"file:{str(cookie_db)}?immutable=1", uri=True)

    # assumes higher ids imply more recent values
    curs = con.execute(
        """
        SELECT id, host, value
        FROM moz_cookies
        WHERE name = 'session' AND host LIKE '%adventofcode.com%'
        ORDER BY id DESC;
        """
    )
    retval = curs.fetchall()
    # print("\n".join(retval))

    if len(retval) > 0:
        # [0]: first result
        # [2]: session value
        # return the actual session cookie value
        return retval[0][2]

    # assume no session value was found with query
    return None


def main():
    cookie_db = find_cookies_file(profiles)
    session = ""

    if cookie_db is not None:
        session = query_cookies_file(cookie_db)
        session = "" if session is None else session

    if session == "":
        # bail if the session cant be found. cookie_db is None or session query failed to return result
        print("!!! adventofcode.com session could not be found !!!")
        return

    meta_dir = Path(__file__).parent.parent.joinpath("meta")
    meta_dir.mkdir(exist_ok=True)
    meta_dir.joinpath(".session").touch()

    with open(meta_dir.joinpath(".session"), "wt") as session_file:
        session_file.write(session)

    print(f"session value written to {meta_dir.joinpath('.session')}")


if __name__ == "__main__":
    main()
