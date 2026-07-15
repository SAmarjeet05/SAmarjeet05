from __future__ import annotations

import heapq

from chronoai.motion.models import CalendarGrid


def _astar(
    start: tuple[int, int],
    target: tuple[int, int],
    cols: int,
    rows: int,
) -> list[tuple[int, int]]:
    """A* shortest path on a cols×rows grid with Manhattan heuristic.
    
    Returns the path including start and target, or empty list if unreachable.
    """
    if start == target:
        return [start]

    def h(node: tuple[int, int]) -> int:
        return abs(node[0] - target[0]) + abs(node[1] - target[1])

    open_heap: list[tuple[int, int, tuple[int, int], list[tuple[int, int]]]] = []
    heapq.heappush(open_heap, (h(start), 0, start, [start]))
    visited: dict[tuple[int, int], int] = {start: 0}

    while open_heap:
        f, g, node, path = heapq.heappop(open_heap)

        if node == target:
            return path

        # Skip stale expansions
        if g > visited.get(node, float("inf")):
            continue

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nb = (node[0] + dx, node[1] + dy)
            if 0 <= nb[0] < cols and 0 <= nb[1] < rows:
                new_g = g + 1
                if new_g < visited.get(nb, float("inf")):
                    visited[nb] = new_g
                    heapq.heappush(open_heap, (new_g + h(nb), new_g, nb, path + [nb]))

    return []


def plan_eat_path(
    grid: CalendarGrid,
    start_pos: tuple[int, int] = (0, 0),
) -> list[tuple[int, int]]:
    """Uses A* to build the eating phase path through all food cells.
    
    Returns only the grid-bounded eating phase path. Off-screen travel
    and the cinematic loop phases are handled by the timeline module.
    """
    food_set: set[tuple[int, int]] = set()
    cols = len(grid.weeks)
    rows = 7

    for col_idx, week in enumerate(grid.weeks):
        for row_idx, day in enumerate(week.days):
            if day.level != "NONE" and day.count > 0:
                food_set.add((col_idx, row_idx))

    current = start_pos
    eat_path: list[tuple[int, int]] = [current]

    while food_set:
        # Pick nearest food cell by Manhattan distance
        closest = min(
            food_set,
            key=lambda f: abs(f[0] - current[0]) + abs(f[1] - current[1]),
        )

        sub_path = _astar(current, closest, cols=cols, rows=rows)
        if not sub_path:
            food_set.discard(closest)
            continue

        eat_path.extend(sub_path[1:])
        current = closest
        food_set.discard(closest)

    return eat_path
