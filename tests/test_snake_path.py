from __future__ import annotations

import datetime
import pytest

from chronoai.motion.models import CalendarGrid, ContributionDay, ContributionWeek
from chronoai.motion.planner import plan_eat_path, _astar
from chronoai.motion.timeline import build_motion_timeline
from chronoai.motion.grid import parse_api_response


def _make_empty_grid(num_weeks: int = 53) -> CalendarGrid:
    """Creates a CalendarGrid with no contributions (all NONE)."""
    weeks = []
    today = datetime.date.today()
    start = today - datetime.timedelta(days=num_weeks * 7)
    for col in range(num_weeks):
        days = []
        for row in range(7):
            date = start + datetime.timedelta(days=col * 7 + row)
            days.append(ContributionDay(date=date, count=0, level="NONE", x=float(col), y=float(row)))
        weeks.append(ContributionWeek(days=days))
    return CalendarGrid(total_contributions=0, weeks=weeks)


def _make_grid_with_contributions(num_weeks: int = 10) -> CalendarGrid:
    """Creates a CalendarGrid with scattered contribution cells."""
    weeks = []
    today = datetime.date.today()
    start = today - datetime.timedelta(days=num_weeks * 7)
    for col in range(num_weeks):
        days = []
        for row in range(7):
            date = start + datetime.timedelta(days=col * 7 + row)
            count = 3 if (col % 3 == 0 and row in [0, 3]) else 0
            level = "SECOND_QUARTILE" if count > 0 else "NONE"
            days.append(ContributionDay(date=date, count=count, level=level, x=float(col), y=float(row)))
        weeks.append(ContributionWeek(days=days))
    total = sum(d.count for w in weeks for d in w.days)
    return CalendarGrid(total_contributions=total, weeks=weeks)


class TestAstar:
    def test_same_start_and_target(self):
        path = _astar((0, 0), (0, 0), cols=53, rows=7)
        assert path == [(0, 0)], "Path from start to itself should only contain the start."

    def test_adjacent_cells(self):
        path = _astar((0, 0), (1, 0), cols=53, rows=7)
        assert path == [(0, 0), (1, 0)], "A* should find 2-node path between adjacent cells."

    def test_path_stays_in_bounds(self):
        path = _astar((0, 0), (52, 6), cols=53, rows=7)
        assert path, "Path should not be empty."
        for col, row in path:
            assert 0 <= col < 53, f"Column {col} out of grid bounds."
            assert 0 <= row < 7, f"Row {row} out of grid bounds."

    def test_path_is_contiguous(self):
        """Consecutive A* steps should only move one cell at a time (Manhattan distance = 1)."""
        path = _astar((5, 2), (30, 5), cols=53, rows=7)
        for i in range(len(path) - 1):
            dc = abs(path[i + 1][0] - path[i][0])
            dr = abs(path[i + 1][1] - path[i][1])
            assert dc + dr == 1, f"Non-contiguous step between {path[i]} and {path[i+1]}."

    def test_astar_optimal_length(self):
        """A* should find a path whose length equals the Manhattan distance + 1."""
        start, end = (0, 0), (10, 3)
        path = _astar(start, end, cols=53, rows=7)
        expected_len = abs(end[0] - start[0]) + abs(end[1] - start[1]) + 1
        assert len(path) == expected_len, f"Expected {expected_len} steps, got {len(path)}."


class TestPlanEatPath:
    def test_eat_path_starts_at_origin(self):
        grid = _make_empty_grid()
        path = plan_eat_path(grid)
        assert path[0] == (0, 0), "Eat path must start at (0, 0)."

    def test_eat_path_is_not_empty(self):
        grid = _make_empty_grid()
        path = plan_eat_path(grid)
        assert len(path) >= 1, "Eat path must have at least one cell."

    def test_all_food_cells_are_visited(self):
        """Every contribution cell must appear in the eating path."""
        grid = _make_grid_with_contributions()
        path = plan_eat_path(grid)
        visited = set(path)
        for col_idx, week in enumerate(grid.weeks):
            for day in week.days:
                if day.level != "NONE" and day.count > 0:
                    pos = (col_idx, int(day.y))
                    assert pos in visited, f"Food cell {pos} was never visited by the snake."

    def test_eat_path_is_contiguous_on_grid(self):
        """Consecutive cells in the eating path should be adjacent (Manhattan dist = 1)."""
        grid = _make_grid_with_contributions()
        path = plan_eat_path(grid)
        for i in range(len(path) - 1):
            dc = abs(path[i + 1][0] - path[i][0])
            dr = abs(path[i + 1][1] - path[i][1])
            assert dc + dr == 1, f"Non-contiguous eat step between {path[i]} and {path[i+1]}."


class TestBuildMotionTimeline:
    def test_timeline_has_required_keys(self):
        grid = _make_empty_grid()
        eat_path = plan_eat_path(grid)
        motion = build_motion_timeline(eat_path, grid_cols=len(grid.weeks), grid_rows=7)
        for key in ("path", "eat_end", "pause_end", "exit_end", "reset_start", "reset_end", "kinetics"):
            assert key in motion, f"Missing key '{key}' in motion timeline."

    def test_timeline_total_path_has_minimum_length(self):
        grid = _make_empty_grid()
        eat_path = plan_eat_path(grid)
        motion = build_motion_timeline(eat_path, grid_cols=len(grid.weeks), grid_rows=7)
        assert len(motion["path"]) >= 130, "Full motion path should be at least 130 steps."

    def test_timeline_phase_order_is_correct(self):
        grid = _make_grid_with_contributions()
        eat_path = plan_eat_path(grid)
        motion = build_motion_timeline(eat_path, grid_cols=len(grid.weeks), grid_rows=7)
        assert motion["eat_end"] <= motion["pause_end"], "Pause must come after eating."
        assert motion["pause_end"] <= motion["reset_start"], "Reset must start after pause."
        assert motion["reset_start"] <= motion["reset_end"], "Reset end must be after reset start."

    def test_timeline_indices_within_path_length(self):
        grid = _make_grid_with_contributions()
        eat_path = plan_eat_path(grid)
        motion = build_motion_timeline(eat_path, grid_cols=len(grid.weeks), grid_rows=7)
        n = len(motion["path"])
        assert motion["eat_end"] < n, "eat_end out of path bounds."
        assert motion["pause_end"] < n, "pause_end out of path bounds."
        assert motion["reset_start"] < n, "reset_start out of path bounds."

    def test_atmosphere_kinetics_are_applied(self):
        grid = _make_empty_grid()
        eat_path = plan_eat_path(grid)
        for atm in ["boot", "inference", "optimization", "research"]:
            motion = build_motion_timeline(eat_path, grid_cols=len(grid.weeks), grid_rows=7, atmosphere=atm)
            assert motion["kinetics"].label.lower() == atm, f"Wrong kinetics label for atmosphere '{atm}'."


class TestParseApiResponse:
    def test_parse_basic_response(self):
        """Parsing should produce correct coordinates for a 2-week example."""
        raw = {
            "totalContributions": 3,
            "weeks": [
                {"contributionDays": [
                    {"date": "2026-01-01", "contributionCount": 0, "weekday": 0, "contributionLevel": "NONE"},
                    {"date": "2026-01-02", "contributionCount": 2, "weekday": 1, "contributionLevel": "FIRST_QUARTILE"},
                ]},
                {"contributionDays": [
                    {"date": "2026-01-08", "contributionCount": 1, "weekday": 0, "contributionLevel": "NONE"},
                ]},
            ]
        }
        grid = parse_api_response(raw, cell_size=10, cell_gap=2, left_padding=30, top_padding=20)
        assert isinstance(grid, CalendarGrid)
        assert len(grid.weeks) == 2
        assert grid.weeks[0].days[0].count == 0
        assert grid.weeks[0].days[1].count == 2
        assert grid.weeks[0].days[0].x == pytest.approx(30.0)
        assert grid.weeks[0].days[0].y == pytest.approx(20.0)
        # Week 1 (second column): x = 30 + 1*(10+2) = 42.0
        assert grid.weeks[1].days[0].x == pytest.approx(42.0)
