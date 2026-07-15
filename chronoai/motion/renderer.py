from __future__ import annotations

import os

from chronoai.motion.fetcher import fetch_contribution_calendar
from chronoai.motion.grid import parse_api_response
from chronoai.motion.palette import PALETTES
from chronoai.motion.planner import plan_eat_path
from chronoai.motion.svg import render_svg
from chronoai.motion.timeline import build_motion_timeline


class ChronoMotionRenderer:
    """Orchestrates the full ChronoMotion Engine pipeline.

    Pipeline:
      Fetch → Parse Grid → Plan Eat Path → Build Motion Timeline → Render SVG
    """

    @staticmethod
    def render_all_atmospheres(
        username: str,
        token: str | None = None,
        output_dir: str = "assets/snake",
    ) -> None:
        os.makedirs(output_dir, exist_ok=True)

        print("[ChronoMotion] Fetching contribution calendar...")
        api_data = fetch_contribution_calendar(username, token)

        print("[ChronoMotion] Parsing calendar grid layout...")
        grid = parse_api_response(api_data)

        print(f"[ChronoMotion] Planning A* eating path ({len(grid.weeks)} weeks)...")
        eat_path = plan_eat_path(grid)

        # Render light + dark SVGs for all 4 atmospheres
        for atmosphere, variants in PALETTES.items():
            print(f"[ChronoMotion] Building motion timeline for '{atmosphere}'...")
            motion = build_motion_timeline(
                eat_path=eat_path,
                grid_cols=len(grid.weeks),
                grid_rows=7,
                atmosphere=atmosphere,
            )

            for mode, palette in variants.items():
                filepath = os.path.join(output_dir, f"snake-{atmosphere}-{mode}.svg")
                print(f"[ChronoMotion] Rendering {filepath}...")

                svg_content = render_svg(
                    grid=grid,
                    palette=palette,
                    motion=motion,
                )

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(svg_content)

                print(f"[ChronoMotion] ✓ {filepath}")
