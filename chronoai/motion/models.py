from __future__ import annotations

import datetime
from dataclasses import dataclass


@dataclass
class ContributionDay:
    date: datetime.date
    count: int
    level: str  # NONE | FIRST_QUARTILE | SECOND_QUARTILE | THIRD_QUARTILE | FOURTH_QUARTILE
    x: float = 0.0
    y: float = 0.0


@dataclass
class ContributionWeek:
    days: list[ContributionDay]


@dataclass
class CalendarGrid:
    total_contributions: int
    weeks: list[ContributionWeek]
