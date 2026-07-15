# ChronoMotion Engine

> ChronoAI v2.0.0 — Native ChronoMotion Engine Reference

## Overview

The ChronoMotion Engine is a fully self-contained motion and rendering engine that:

1. **Fetches** the user's GitHub contribution calendar via the GraphQL API
2. **Parses** it into clean grid coordinate systems
3. **Plans** paths to all contribution food cells using the **A\*** search algorithm
4. **Schedules** detailed timelines containing eating, pausing, exiting, resetting, and re-entering phases
5. **Renders** glowing, animated SVGs with premium animations like cascading wave resets, Pac-Man overshoot momentum, and theme-specific Kinetics (tail length and step speeds)

---

## Module Structure

```
chronoai/motion/
├── __init__.py     # Exports ChronoMotionRenderer & version Metadata
├── models.py       # Data classes: ContributionDay, ContributionWeek, CalendarGrid
├── fetcher.py      # GraphQL fetcher client with offline mock fallback
├── grid.py         # Grid mapping, coordinate positioning, month/weekday labels
├── planner.py      # A* pathfinder: computes step-by-step paths to food cells
├── timeline.py     # Motion planner: computes Bézier-like exits, pauses, and re-entry overshoots
├── palette.py      # Visual palettes configurations (including glow/eye colors)
└── svg.py          # SVG scene compiler: coordinates, cascading wave resets, head pulsing, and tail segments
```

---

## Phase 1 — Data Layer (`models.py` + `fetcher.py`)

Identical to v1.0.0, the fetcher resolves contribution data and maps it to `CalendarGrid`. If `GITHUB_TOKEN` is missing, a realistic random mock generator simulates active contribution grids.

---

## Phase 2 — A\* Pathfinder (`planner.py`)

Instead of standard BFS, ChronoMotion Engine uses **A\* search** with a Manhattan distance heuristic to calculate optimal paths:

- Evaluates `f(n) = g(n) + h(n)` to move from cell to cell
- Consumes all contribution food cells sequentially in a greedy order (nearest first)
- Generates a grid-bounded path containing only the active eating phase steps

---

## Phase 3 — Cinematic Timeline Planner (`timeline.py`)

Extends the grid path with off-screen loop and physical feedback actions:

- **AI Pause**: Repeats the final eaten position for a short duration (`pause_steps`)
- **Bézier Exit Curve**: Simulates inertia by curving diagonal steps off-screen to the right, then wrapping around the bottom of the calendar
- **Pac-Man Overshoot**: Re-enters from the left edge by overshooting the start cell to column 1 and pulling back to `(0, 0)` for a natural momentum effect

---

## Phase 4 — Visual Rendering (`svg.py`)

Compiles the final SMIL SVG. Upgrades include:

- **Pulsing Head Glow**: Head size and opacity animate independently during the AI pause window to simulate a "thinking" pulse
- **Cascading Wave Reset**: Cell refill timing is staggered linearly based on column index (`x`), making the calendar restore in a beautiful left-to-right wave while the snake is off-screen
- **Theme-specific Kinetics**:
  - `boot`: Slow step speed (120ms), long tail (7 segments)
  - `inference`: Fast step speed (60ms), short tail (4 segments)
  - `optimization`: Smooth step speed (80ms), balanced tail (5 segments)
  - `research`: Deliberate step speed (100ms), glowing pulse focus (6 segments)
