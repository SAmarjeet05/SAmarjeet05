from __future__ import annotations

import datetime
from typing import Any

from chronoai.motion.models import CalendarGrid, ContributionDay, ContributionWeek


def parse_api_response(
    api_data: dict[str, Any],
    cell_size: float = 10.0,
    cell_gap: float = 2.0,
    left_padding: float = 30.0,
    top_padding: float = 20.0,
) -> CalendarGrid:
    """Parses raw GraphQL response dictionary into a structured CalendarGrid model with layout coordinates."""
    raw_weeks = api_data.get("weeks", [])
    total_contributions = api_data.get("totalContributions", 0)

    weeks = []
    for col_idx, raw_week in enumerate(raw_weeks):
        days = []
        raw_days = raw_week.get("contributionDays", [])
        for row_idx, raw_day in enumerate(raw_days):
            date_str = raw_day.get("date")
            date_val = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            count = raw_day.get("contributionCount", 0)
            level = raw_day.get("contributionLevel", "NONE")

            x = left_padding + col_idx * (cell_size + cell_gap)
            y = top_padding + row_idx * (cell_size + cell_gap)

            days.append(
                ContributionDay(
                    date=date_val,
                    count=count,
                    level=level,
                    x=x,
                    y=y,
                )
            )
        weeks.append(ContributionWeek(days=days))

    return CalendarGrid(total_contributions=total_contributions, weeks=weeks)


def get_month_labels(
    grid: CalendarGrid,
    cell_size: float = 10.0,
    cell_gap: float = 2.0,
    left_padding: float = 30.0,
) -> list[tuple[float, str]]:
    """Calculates column X coordinates for month header labels, preventing overlap."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    labels: list[tuple[float, str]] = []
    prev_month = None

    for col_idx, week in enumerate(grid.weeks):
        if not week.days:
            continue
        
        current_month = week.days[0].date.month
        if current_month != prev_month:
            month_name = months[current_month - 1]
            x = left_padding + col_idx * (cell_size + cell_gap)
            labels.append((x, month_name))
            prev_month = current_month

    # Stagger/filter month labels that are too close (at least 3 columns apart)
    filtered_labels = []
    last_x = -100.0
    for x, name in labels:
        if x - last_x >= 3.0 * (cell_size + cell_gap):
            filtered_labels.append((x, name))
            last_x = x

    return filtered_labels
