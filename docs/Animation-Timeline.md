# Animation Timeline

> ChronoMotion Engine v2.0.0 — Frame-by-Frame Animation Reference

## Overview

The ChronoMotion Engine renders a seamless, looping animation that never visibly resets.
The trick: the contribution grid is restored **while the snake is completely off-screen**.
The viewer perceives a continuous, infinite loop.

---

## Phase Map (Full Loop)

```
 ────────────────────────────────────────────────────────────────────
 0%                                                              100%
 │                                                                  │
 ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 │←──── Eating (88%) ────→│Pause│←── Exit ──→│Reset│← Entry →│
 0%                       88%  91%           95%  97%        100%
```

---

## Phase 1: Eating — `0% → 88%`

The snake uses **A\* pathfinding** to greedily visit all contribution cells with `count > 0`.

**Visually:**
```
□□□□□□□□□□□□□□□□□□
□□□□□□□□□□□□□□□□□□   🐍 chasing food
□□□□□□□□□□□□□□□□□□
```

**Per-cell keyframe sequence:**

| Keyframe | Color | Trigger |
|---|---|---|
| `0.0` | Original contribution color | Animation starts |
| `t_eat - 1 step` | Original contribution color | Snake approaching |
| `t_eat` | Snake glow color (flash!) | Snake arrives and eats |
| `t_eat + 1 step` | Empty cell color | Contribution consumed |
| (holds here until reset) | Empty cell color | Waiting for wave reset |

---

## Phase 2: AI Thinking Pause — `88% → 91%`

The snake stops at the last food cell. The **head pulses**.

**Head animation during pause:**

| Frame | Width | Opacity | Effect |
|---|---|---|---|
| Pause start | `10px` | `1.0` | Normal |
| Pause mid | `10 × scale_factor` | `0.6` | Expanded, glowing |
| Pause end | `10px` | `1.0` | Contracted back |

The `scale_factor` (head expansion) is **atmosphere-specific**:

| Atmosphere | Scale | Feel |
|---|---|---|
| Boot | `1.25×` | Large, slow pulse |
| Inference | `1.10×` | Tight, minimal |
| Optimization | `1.18×` | Smooth, fluid |
| Research | `1.30×` | Wide, deliberate |

**Why opacity and not just size?**
Animating opacity creates a **brightness pulse** effect — the head appears to glow brighter at its peak, then settle. This is more cinematic than a color shift.

---

## Phase 3: Exit — `91% → 95%`

The snake exits the grid via a **Bézier-approximated diagonal path**:

```
                    ╲
□□□□□□□□□□□□□□□□□□ 🐍
□□□□□□□□□□□□□□□□□□   ↘
□□□□□□□□□□□□□□□□□□     ↘
                        ──────────────────►
```

The path computes:
1. **8 diagonal steps** (col+1, row+1) — the curved departure
2. **Horizontal exit** to `col = grid_cols + 1` (right off-screen)
3. **Vertical drop** to `row = grid_rows + 1` (below the calendar)
4. **Left sweep** to `col = -3` (off-screen left)
5. **Rise** to `row = 0`
6. **Re-entry** from `col = -3` to `col = 1` (Pac-Man entry, +1 overshoot)
7. **Settle** back to `(0, 0)`

The snake segments smoothly follow this off-screen arc. To the viewer, the snake disappears — and the grid resets silently.

---

## Phase 4: Invisible Grid Reset — `95% → 97%`

While the snake is fully off-screen (traveling below the grid), all eaten cells **cascade back** left-to-right like a wave:

```
□□□□□□□□□□□□□□□□□
■■□□□□□□□□□□□□□□□    ← restoring from left
■■■■■■□□□□□□□□□□□
■■■■■■■■■■□□□□□□□
■■■■■■■■■■■■■■□□□
■■■■■■■■■■■■■■■■■    ← complete
```

**Per-cell restore formula:**
```
wave_fraction = col_index / (total_cols - 1)
t_restore = reset_start + wave_fraction × (reset_end - reset_start)
```

This staggers each column's restore time, producing the satisfying sweep effect. Duration ≈ 0.4–0.6 seconds real-time.

---

## Phase 5: Re-entry — `97% → 100%`

The snake re-enters from the left off-screen. The path includes a **+1 overshoot**:

```
        ← col -3   col -2   col -1   col 0    col 1
            🐍 →     →        →       →   →(!)  ←back
```

The extra step to `col = 1` and the step back to `col = 0` give the snake a **momentum illusion** — as if it arrived with velocity and eased into position.

At `100%`, the path returns exactly to `(0, 0)` — completing the seamless loop.

---

## Atmosphere-Specific Motion Characteristics

Each atmosphere produces a **distinct personality** that can be recognized by movement alone:

| Atmosphere | Step Speed | Tail Length | Head Scale | Character |
|---|---|---|---|---|
| **Boot** | 120ms | 7 segments | 1.25× | Slow, gentle, long flowing tail |
| **Inference** | 60ms | 4 segments | 1.10× | Fast, precise, minimal tail |
| **Optimization** | 80ms | 5 segments | 1.18× | Smooth, fluid, balanced |
| **Research** | 100ms | 6 segments | 1.30× | Deliberate, glowing, contemplative |

---

## Module Mapping

| Timeline Phase | Module |
|---|---|
| Food cell detection | `planner.py` — `plan_eat_path()` |
| A* cell-to-cell paths | `planner.py` — `_astar()` |
| Pause steps + kinetics | `timeline.py` — `MotionKinetics`, `build_motion_timeline()` |
| Bézier exit path | `timeline.py` — `_bezier_exit_steps()` |
| Grid reset keyframes | `svg.py` — per-cell `<animate>` with `wave_fraction` |
| Head pulse animation | `svg.py` — `<animate>` on `width`, `height`, `opacity` |
| Glow filter rendering | `svg.py` — `<filter id="headglow">` |
| SVG scene assembly | `svg.py` — `render_svg()` |
| Pipeline orchestration | `renderer.py` — `ChronoMotionRenderer.render_all_atmospheres()` |
