# Rendering Pipeline

> ChronoAI v2.0.0 — README Rendering Pipeline Reference

## Overview

The README rendering pipeline transforms a single `README.template.md` into a theme-aware, atmosphere-specific Markdown file. The pipeline is orchestrated by `READMEBuilder` in `chronoai/builder.py`.

---

## Pipeline Stages

```
[1] Atmosphere Resolution
        ↓
[2] Theme Loading & Merging
        ↓
[3] Cache Validation
        ↓
[4] Template Rendering
        ↓
[5] Plugin Section Injection
        ↓
[6] Output Writing
        ↓
[7] Cache Update
```

---

## Stage 1 — Atmosphere Resolution

`AtmosphereResolver` reads the current time in IST (configurable via `config.json`) and returns one of four mode strings:

| IST Time | Mode |
|---|---|
| 00:00 – 06:00 | `boot` |
| 06:00 – 11:00 | `inference` |
| 11:00 – 17:30 | `optimization` |
| 17:30 – 00:00 | `research` |

The mode can be overridden via `--mode` or `--time` CLI flags for testing.

---

## Stage 2 — Theme Loading & Merging

`ThemeLoader` loads `themes/{mode}.json` and deep-merges it on top of `themes/base.json`:

```python
merged_theme = deep_merge(base_theme, atmosphere_theme)
```

The resulting object is the single source of truth for all visual configuration used downstream.

---

## Stage 3 — Cache Validation

The cache system (`chronoai/cache/`) uses **SHA-256 content hashing** to determine if the current configuration would produce a different README than the stored cache.

The hash input includes:
- The raw template content
- The merged theme JSON
- The resolved mode string

If the computed hash matches the stored `.sha256` file, the cached `.md` file is copied directly to output — skipping rendering entirely.

**Override with `--no-cache`** to force a fresh render regardless.

---

## Stage 4 — Template Rendering

The template engine reads `README.template.md` and replaces all `{{PLACEHOLDER}}` tokens:

| Placeholder | Replaced With |
|---|---|
| `{{TYPING_SVG}}` | Animated typing SVG URL (from `stats.py`) |
| `{{SNAKE_PICTURE}}` | `<picture>` tag with light/dark SVG paths |
| `{{STREAK}}` | GitHub streak card `<picture>` tag |
| `{{GRAPH}}` | Activity graph `<picture>` tag |
| `{{DIVIDER_PATH}}` | Path to atmosphere-specific divider SVG |
| `{{ASSET_*}}` | Various asset paths from the theme |

---

## Stage 5 — Plugin Section Injection

Plugins in `chronoai/plugins/` generate self-contained Markdown sections that are injected at designated points in the template. Each plugin:

- Receives the merged `theme` and `config` context
- Returns a complete Markdown string
- Has no awareness of other plugins

Example plugins:
- **Skills plugin** — renders the technology stack section
- **Snake plugin** — builds the `<picture>` element for the contribution SVG
- **Stats plugin** — generates the GitHub stats/streak/graph HTML

---

## Stage 6 — Output Writing

The rendered Markdown is written to two locations simultaneously:

1. `README.md` — the root profile README consumed by GitHub
2. `generated/README.md` — a versioned copy for diffing and history

---

## Stage 7 — Cache Update

After a fresh render, the cache is updated:
- `cache/{mode}.md` ← the rendered output
- `cache/{mode}.sha256` ← the new content hash

Subsequent runs within the same atmosphere window will hit the cache immediately.

---

## Preview Files

When `--build-cache` is run, preview copies are also generated:
- `preview/{mode}.md` ← human-readable preview of each atmosphere's output

These are useful for reviewing all themes without switching the active atmosphere.

---

## CLI Reference

```bash
# Generate README for the current atmosphere (cache-aware)
python generate_readme.py

# Force fresh generation (bypass cache)
python generate_readme.py --no-cache

# Force a specific atmosphere
python generate_readme.py --mode research

# Simulate a specific time (for testing)
python generate_readme.py --time 22:00

# Rebuild all caches and ChronoMotion SVGs
python generate_readme.py --build-cache

# Rebuild ChronoMotion SVGs only
python generate_readme.py --build-contribution

# Print debug info for current run
python generate_readme.py --debug
```
