from __future__ import annotations

import datetime
import json
import random
import urllib.request
from typing import Any


def _generate_mock_calendar() -> dict[str, Any]:
    # Align to Sunday of 52 weeks ago to get a complete 53-week grid
    today = datetime.date.today()
    days_to_subtract = (today.weekday() + 1) % 7 + 52 * 7
    start_date = today - datetime.timedelta(days=days_to_subtract)

    weeks = []
    total = 0
    current_date = start_date
    for _ in range(53):
        days = []
        for d in range(7):
            count = random.choices([0, random.randint(1, 10)], weights=[65, 35])[0]
            if count == 0:
                level = "NONE"
            elif count < 3:
                level = "FIRST_QUARTILE"
            elif count < 6:
                level = "SECOND_QUARTILE"
            elif count < 9:
                level = "THIRD_QUARTILE"
            else:
                level = "FOURTH_QUARTILE"

            days.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "contributionCount": count,
                "weekday": d,
                "contributionLevel": level,
            })
            total += count
            current_date += datetime.timedelta(days=1)
        weeks.append({"contributionDays": days})

    return {
        "totalContributions": total,
        "weeks": weeks,
    }


def fetch_contribution_calendar(username: str, token: str | None = None) -> dict[str, Any]:
    """Fetches raw contribution grid from GitHub GraphQL API with local mock fallback."""
    if not token:
        print("[ChronoMotion Fetcher] No GITHUB_TOKEN. Using mock contribution data...")
        return _generate_mock_calendar()

    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
                weekday
                contributionLevel
              }
            }
          }
        }
      }
    }
    """
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "ChronoMotion-Engine",
    }
    payload = {
        "query": query,
        "variables": {"username": username},
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if "errors" in res_data:
                raise RuntimeError(f"GraphQL Errors: {res_data['errors']}")
            
            user_data = res_data.get("data", {}).get("user")
            if not user_data:
                raise RuntimeError(f"User '{username}' not found.")
            
            return user_data["contributionsCollection"]["contributionCalendar"]
    except Exception as exc:
        print(f"[ChronoMotion Fetcher] Fetch failed: {exc}. Falling back to mock data...")
        return _generate_mock_calendar()
