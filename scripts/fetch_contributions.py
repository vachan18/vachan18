#!/usr/bin/env python3
"""
Fetch the public contribution calendar for a GitHub user.

Scrapes https://github.com/users/<username>/contributions (no token needed)
and writes data/contributions.json with raw day-level data plus derived stats.
"""

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "vachan18"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def fetch():
    resp = requests.get(URL, headers={"Accept": "text/html"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []

    # Build a map of id -> tooltip text from tool-tip elements
    tip_map = {}
    for tip_el in soup.select("tool-tip"):
        for_id = tip_el.get("for", "")
        if for_id:
            tip_map[for_id] = tip_el.get_text(strip=True)

    for td in soup.select("td.ContributionCalendar-day"):
        date = td.get("data-date")
        if not date:
            continue
        level = int(td.get("data-level", 0))
        count = 0
        td_id = td.get("id", "")
        tip_text = tip_map.get(td_id, "")
        if tip_text:
            m = re.search(r"(\d+)\s+contribution", tip_text)
            if m:
                count = int(m.group(1))
        days.append({"date": date, "count": count, "level": level})

    days.sort(key=lambda d: d["date"])

    # Derived stats
    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}

    # Streaks
    current_streak = 0
    longest_streak = 0
    streak = 0
    for d in reversed(days):
        if d["count"] > 0:
            streak += 1
        else:
            if streak > longest_streak:
                longest_streak = streak
            if current_streak == 0:
                current_streak = streak
            streak = 0
    longest_streak = max(longest_streak, streak)
    if current_streak == 0:
        current_streak = streak

    # Monthly totals
    monthly = {}
    for d in days:
        m = d["date"][:7]
        monthly[m] = monthly.get(m, 0) + d["count"]

    data = {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total": total,
        "best_day": {"date": best["date"], "count": best["count"]},
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "monthly": monthly,
        "days": days,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))
    print(f"[OK] Wrote {len(days)} days ({total} contributions) -> {OUT}")


if __name__ == "__main__":
    fetch()
