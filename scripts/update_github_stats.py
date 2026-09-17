#!/usr/bin/env python3
"""Refresh the GitHub Stats table in README.md from live contribution data."""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import urllib.request

USER = "eswar007206"
README = os.path.join(os.path.dirname(__file__), "..", "README.md")
MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


def get_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "eswar007206-readme-stats",
            "Accept": "application/vnd.github+json",
        },
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def fmt_num(n: int) -> str:
    return f"{n:,}"


def fmt_date(day: dt.date) -> str:
    return f"{day.day} {MONTHS[day.month - 1]} {day.year}"


def fetch_days(start_year: int, end_year: int) -> list[tuple[dt.date, int]]:
    days: list[tuple[dt.date, int]] = []
    for year in range(start_year, end_year + 1):
        data = get_json(
            f"https://github-contributions-api.jogruber.de/v4/{USER}?y={year}"
        )
        for item in data.get("contributions", []):
            day = dt.date.fromisoformat(item["date"])
            days.append((day, int(item.get("count") or 0)))
    return days


def longest_streak(days: list[tuple[dt.date, int]]) -> int:
    best = current = 0
    for _, count in sorted(days):
        if count > 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def build_table(user: dict, days: list[tuple[dt.date, int]]) -> str:
    today = dt.date.today()
    days = [(day, count) for day, count in days if day <= today]
    created = dt.date.fromisoformat(user["created_at"][:10])
    last365_start = today - dt.timedelta(days=364)
    years = sorted({day.year for day, _ in days})
    by_year = {year: 0 for year in years}
    for day, count in days:
        by_year[day.year] += count

    best_day, best_count = max(days, key=lambda item: (item[1], item[0]))
    year_rows = "\n".join(
        f"| **{year}** | {fmt_num(by_year[year])} |" for year in years
    )

    return f"""<!-- github-stats:start -->
## GitHub Stats

| | |
| --- | --- |
| **Projects** | {user["public_repos"]} public repositories |
| **Contributions** | {fmt_num(sum(count for _, count in days))} |
| **Last 365 days** | {fmt_num(sum(count for day, count in days if last365_start <= day <= today))} |
{year_rows}
| **Started on** | {fmt_date(created)} |
| **Highest in a day** | {fmt_num(best_count)} contributions ({fmt_date(best_day)}) |
| **Longest streak** | {longest_streak(days)} days |
| **Active days** | {sum(1 for _, count in days if count > 0)} |
<!-- github-stats:end -->"""


def main() -> None:
    readme_path = os.path.normpath(README)
    user = get_json(f"https://api.github.com/users/{USER}")
    created_year = int(user["created_at"][:4])
    days = fetch_days(created_year, dt.date.today().year)
    table = build_table(user, days)

    with open(readme_path, encoding="utf-8") as handle:
        readme = handle.read()

    pattern = re.compile(
        r"<!-- github-stats:start -->.*?<!-- github-stats:end -->",
        re.DOTALL,
    )
    if not pattern.search(readme):
        raise SystemExit("Stats markers not found in README.md")

    updated = pattern.sub(table, readme)
    if updated != readme:
        with open(readme_path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(updated)
        print("README stats updated")
    else:
        print("README stats already current")


if __name__ == "__main__":
    main()
