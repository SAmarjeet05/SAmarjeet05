from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MotionKinetics:
    """Defines atmosphere-specific snake behavior and timing."""
    step_ms: int         # Milliseconds per grid step
    tail_length: int     # Number of trailing segments to render
    pause_steps: int     # How many steps the AI thinking pause lasts (~0.5s relative)
    head_glow_scale: float  # Head expansion factor during pause (1.0 = no expansion)
    label: str           # Human-readable atmosphere name


# Per-atmosphere kinetics — each feels distinctly different
KINETICS: dict[str, MotionKinetics] = {
    "boot": MotionKinetics(
        step_ms=120,
        tail_length=7,
        pause_steps=5,
        head_glow_scale=1.25,
        label="Boot",
    ),
    "inference": MotionKinetics(
        step_ms=60,
        tail_length=4,
        pause_steps=3,
        head_glow_scale=1.10,
        label="Inference",
    ),
    "optimization": MotionKinetics(
        step_ms=80,
        tail_length=5,
        pause_steps=4,
        head_glow_scale=1.18,
        label="Optimization",
    ),
    "research": MotionKinetics(
        step_ms=100,
        tail_length=6,
        pause_steps=6,
        head_glow_scale=1.30,
        label="Research",
    ),
}


def _bezier_exit_steps(
    start: tuple[int, int],
    cols: int,
    rows: int,
) -> list[tuple[int, int]]:
    """Generates a smooth Bézier-like curve from the final food cell heading off-screen.
    
    Uses quadratic interpolation in grid-cell space, curving diagonally down-right
    before travelling below the grid and back around.
    """
    path: list[tuple[int, int]] = []
    c, r = start

    # Phase A: curve diagonally toward the bottom-right (8 diagonal steps)
    for _ in range(8):
        c = min(c + 1, cols)
        r = min(r + 1, rows)
        path.append((c, r))

    # Phase B: exit horizontally off the right edge to col cols+1
    while c <= cols:
        c += 1
        path.append((c, r))

    # Phase C: travel below the grid: drop to row rows+1 (off-screen below)
    while r <= rows:
        r += 1
        path.append((c, r))

    # Phase D: sweep left all the way to col -3 (off-screen left)
    while c > -3:
        c -= 1
        path.append((c, r))

    # Phase E: rise up to row 0
    while r > 0:
        r -= 1
        path.append((c, r))

    # Phase F: enter from col -3 to col 1 (Pac-Man entry with +1 overshoot)
    while c < 1:
        c += 1
        path.append((c, r))

    # Phase G: settle back to (0, 0) — single step back
    path.append((0, 0))

    return path


def build_motion_timeline(
    eat_path: list[tuple[int, int]],
    grid_cols: int,
    grid_rows: int,
    atmosphere: str = "optimization",
) -> dict[str, Any]:
    """Assembles the complete cinematic motion timeline from eating through seamless re-entry.

    Timeline phases (proportional):
      0.0% – 88%: Eating (A* guided food chasing)
      88% – 91%: AI thinking pause (snake holds at last food cell, head pulses)
      91% – 95%: Bézier exit curve + border travel (off-screen)
      95% – 97%: Off-screen (cells cascade-reset while snake invisible)
      97% – 100%: Pac-Man re-entry with +1 overshoot, settling at (0, 0)

    Returns a dict with:
      - 'path': complete list of (col, row) steps
      - 'eat_end': index where eating phase ends
      - 'pause_end': index where pause phase ends
      - 'exit_end': index where exit phase ends
      - 'reset_start': index where the wave reset begins (mid off-screen)
      - 'reset_end': index where the wave reset ends
      - 'kinetics': MotionKinetics for this atmosphere
    """
    kinetics = KINETICS.get(atmosphere, KINETICS["optimization"])

    # Phase 1: Eating path (from planner)
    eat_end = len(eat_path) - 1

    # Phase 2: AI thinking pause - hold the last position for pause_steps
    last_pos = eat_path[-1]
    pause_path = [last_pos] * kinetics.pause_steps
    pause_end = eat_end + kinetics.pause_steps

    # Phase 3+4+5: Bézier exit, off-screen travel, and Pac-Man re-entry
    loop_path = _bezier_exit_steps(last_pos, cols=grid_cols, rows=grid_rows)

    # Calculate where the loop is fully off-screen (used for wave reset window)
    # Off-screen is when col <= -1 or col >= grid_cols — this starts partway through loop_path
    off_screen_start_in_loop = 0
    for i, (c, r) in enumerate(loop_path):
        if c < 0 or c >= grid_cols:
            off_screen_start_in_loop = i
            break

    t_exit_end = pause_end + off_screen_start_in_loop
    t_reset_start = pause_end + off_screen_start_in_loop
    t_reset_end = pause_end + len(loop_path) - 10  # reset completes well before re-entry

    # Assemble full path
    full_path = eat_path + pause_path + loop_path

    return {
        "path": full_path,
        "eat_end": eat_end,
        "pause_end": pause_end,
        "exit_end": t_exit_end,
        "reset_start": t_reset_start,
        "reset_end": t_reset_end,
        "kinetics": kinetics,
    }
