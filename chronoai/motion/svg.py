from __future__ import annotations

from typing import Any

from chronoai.motion.grid import get_month_labels
from chronoai.motion.models import CalendarGrid
from chronoai.motion.palette import MotionPalette
from chronoai.motion.timeline import MotionKinetics


def _level_to_color(level_name: str, palette: MotionPalette) -> str:
    if level_name == "FIRST_QUARTILE":
        return palette.levels[1]
    elif level_name == "SECOND_QUARTILE":
        return palette.levels[2]
    elif level_name == "THIRD_QUARTILE":
        return palette.levels[3]
    elif level_name == "FOURTH_QUARTILE":
        return palette.levels[4]
    return palette.levels[0]


def render_svg(
    grid: CalendarGrid,
    palette: MotionPalette,
    motion: dict[str, Any],
    cell_size: float = 10.0,
    cell_gap: float = 2.0,
    left_padding: float = 30.0,
    top_padding: float = 20.0,
) -> str:
    """Renders the full ChronoMotion SVG scene.

    Features:
    - Pixel-space Bézier exit curve
    - AI thinking pause with pulsing head glow
    - Left-to-right cascading grid reset wave
    - Pac-Man re-entry with +1 overshoot
    - Theme-specific tail length and step speed
    - Neon glow filter on head segments
    """
    width = 675
    height = 135

    snake_path: list[tuple[int, int]] = motion["path"]
    eat_end: int = motion["eat_end"]
    pause_end: int = motion["pause_end"]
    reset_start: int = motion["reset_start"]
    reset_end: int = motion["reset_end"]
    kinetics: MotionKinetics = motion["kinetics"]

    path_len = len(snake_path)
    dur = f"{path_len * (kinetics.step_ms / 1000.0):.1f}s"

    # Pre-compute first-visit times for all grid positions
    visit_times: dict[tuple[int, int], int] = {}
    for idx, pos in enumerate(snake_path):
        if pos not in visit_times:
            visit_times[pos] = idx

    # ── SVG DOCUMENT ──────────────────────────────────────────────────────────
    svg: list[str] = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')

    # ── STYLES ────────────────────────────────────────────────────────────────
    svg.append(f"""  <style>
    svg {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background: {palette.bg};
      border-radius: 8px;
    }}
    .month-label {{
      font-size: 9px; fill: {palette.text}; font-weight: 500; opacity: 0.8;
    }}
    .wday-label {{
      font-size: 9px; fill: {palette.text}; font-weight: 500; opacity: 0.65;
    }}
    .legend-text {{
      font-size: 9px; fill: {palette.text}; opacity: 0.65;
    }}
  </style>""")

    # ── DEFS: GLOW FILTER + EYE GLOW ─────────────────────────────────────────
    svg.append(f"""  <defs>
    <!-- Neon halo for the snake head -->
    <filter id="headglow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.2" result="blur" />
      <feComponentTransfer in="blur" result="colored_blur">
        <feFuncA type="linear" slope="0.9" />
      </feComponentTransfer>
      <feMerge>
        <feMergeNode in="colored_blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <!-- Subtler halo for trailing segments -->
    <filter id="tailglow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.4" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
""")

    # ── MONTH LABELS ──────────────────────────────────────────────────────────
    month_labels = get_month_labels(grid, cell_size, cell_gap, left_padding)
    for x, name in month_labels:
        svg.append(f'  <text x="{x}" y="12" class="month-label">{name}</text>')

    # ── WEEKDAY LABELS ────────────────────────────────────────────────────────
    for name, row_idx in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        y = top_padding + row_idx * (cell_size + cell_gap) + 8.5
        svg.append(f'  <text x="8" y="{y}" class="wday-label">{name}</text>')

    # ── CONTRIBUTION GRID CELLS ───────────────────────────────────────────────
    svg.append("  <!-- Contribution Grid -->")
    for col_idx, week in enumerate(grid.weeks):
        for row_idx, day in enumerate(week.days):
            orig = _level_to_color(day.level, palette)
            cell_pos = (col_idx, row_idx)

            if day.level != "NONE" and cell_pos in visit_times:
                t_eat = visit_times[cell_pos]

                # Eat keyframe proportions
                p_eat = t_eat / path_len
                p_flash = min(p_eat + 0.012, (eat_end + 1) / path_len)

                # Cascading wave reset: stagger the restore time by column position
                # so cells fill back left-to-right during the off-screen window
                wave_fraction = col_idx / max(len(grid.weeks) - 1, 1)
                p_restore = (reset_start / path_len) + wave_fraction * (
                    (reset_end - reset_start) / path_len
                )
                p_restore = min(p_restore, 0.99)

                # Build keyframe sequence ensuring strict monotonic ordering
                keytimes = []
                colors = []
                def _add(t: float, c: str) -> None:
                    t = round(max(0.0, min(1.0, t)), 4)
                    if not keytimes or t - keytimes[-1] > 1e-4:
                        keytimes.append(t)
                        colors.append(c)

                _add(0.0, orig)
                _add(p_eat - 0.005, orig)
                _add(p_eat, palette.snake)
                _add(p_flash, palette.levels[0])
                _add(p_restore - 0.005, palette.levels[0])
                _add(p_restore, orig)
                _add(1.0, orig)

                kt_str = ";".join(f"{t:.4f}" for t in keytimes)
                cl_str = ";".join(colors)

                svg.append(
                    f'  <rect x="{day.x:.1f}" y="{day.y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="{orig}">\n'
                    f'    <animate attributeName="fill" values="{cl_str}" keyTimes="{kt_str}" dur="{dur}" repeatCount="indefinite" />\n'
                    f'  </rect>'
                )
            else:
                svg.append(f'  <rect x="{day.x:.1f}" y="{day.y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="{orig}" />')

    # ── LEGEND ────────────────────────────────────────────────────────────────
    legend_x = width - 110
    legend_y = height - 18
    svg.append(f'  <text x="{legend_x - 30}" y="{legend_y + 8}" class="legend-text" text-anchor="end">Less</text>')
    for i, lvl_color in enumerate(palette.levels):
        svg.append(f'  <rect x="{legend_x + i * 12}" y="{legend_y}" width="10" height="10" rx="1.5" fill="{lvl_color}" />')
    svg.append(f'  <text x="{legend_x + 5 * 12}" y="{legend_y + 8}" class="legend-text">More</text>')

    # ── SNAKE BODY SEGMENTS ───────────────────────────────────────────────────
    svg.append("  <!-- ChronoMotion Snake -->")
    n_segments = kinetics.tail_length

    for k in range(n_segments):
        seg_coords = [snake_path[0]] * k + snake_path[:-k] if k > 0 else snake_path

        x_vals = ";".join(
            f"{left_padding + col * (cell_size + cell_gap):.1f}" for col, row in seg_coords
        )
        y_vals = ";".join(
            f"{top_padding + row * (cell_size + cell_gap):.1f}" for col, row in seg_coords
        )

        opacity = round(1.0 - k * (0.75 / max(n_segments - 1, 1)), 3)
        filter_attr = ' filter="url(#headglow)"' if k == 0 else (' filter="url(#tailglow)"' if k == 1 else "")

        if k == 0:
            # ── HEAD: has AI-pause pulse (expand + brightness glow) ───────────
            p_pause_start = eat_end / path_len
            p_pause_mid = (eat_end + kinetics.pause_steps // 2) / path_len
            p_pause_end = pause_end / path_len

            # Head size pulse: normal → expanded → normal
            size_vals = f"{cell_size};{cell_size * kinetics.head_glow_scale:.2f};{cell_size}"
            size_kt = f"0;{p_pause_mid:.4f};{p_pause_end:.4f}"

            # Head opacity pulse: 1.0 → glow_peak → 1.0
            opacity_vals = f"1;0.6;1;0.6;1"
            opacity_kt = f"0;{p_pause_start:.4f};{p_pause_mid:.4f};{p_pause_end - 0.01:.4f};{p_pause_end:.4f}"

            svg.append(
                f'  <rect width="{cell_size}" height="{cell_size}" rx="3"{filter_attr} fill="{palette.glow_color}" opacity="1">\n'
                f'    <animate attributeName="x" values="{x_vals}" dur="{dur}" repeatCount="indefinite" />\n'
                f'    <animate attributeName="y" values="{y_vals}" dur="{dur}" repeatCount="indefinite" />\n'
                f'    <animate attributeName="width" values="{size_vals}" keyTimes="{size_kt}" dur="{dur}" repeatCount="indefinite" />\n'
                f'    <animate attributeName="height" values="{size_vals}" keyTimes="{size_kt}" dur="{dur}" repeatCount="indefinite" />\n'
                f'    <animate attributeName="opacity" values="{opacity_vals}" keyTimes="{opacity_kt}" dur="{dur}" repeatCount="indefinite" />\n'
                f'  </rect>'
            )
        else:
            svg.append(
                f'  <rect width="{cell_size}" height="{cell_size}" rx="2.5"{filter_attr} fill="{palette.snake}" opacity="{opacity:.3f}">\n'
                f'    <animate attributeName="x" values="{x_vals}" dur="{dur}" repeatCount="indefinite" />\n'
                f'    <animate attributeName="y" values="{y_vals}" dur="{dur}" repeatCount="indefinite" />\n'
                f'  </rect>'
            )

    svg.append("</svg>\n")
    return "\n".join(svg)
