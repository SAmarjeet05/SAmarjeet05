# Architecture

> ChronoAI v2.0.0 — System Architecture Overview

## Overview

ChronoAI is a fully self-contained GitHub profile automation system. It resolves the current "atmosphere" (a time-of-day creative theme), generates a pixel-perfect, animated README, and renders its own contribution calendar SVGs — all in Python with no external runtime services required.

---

## High-Level Data Flow

```
┌─────────────────────────────────────────────────────┐
│                  generate_readme.py                 │
│               (CLI entry point)                     │
└──────────────┬──────────────────────┬───────────────┘
               │                      │
    ┌──────────▼──────┐    ┌──────────▼──────────────┐
    │  READMEBuilder  │    │  ChronoMotionRenderer   │
    │  (README gen)   │    │  (SVG Scene gen)        │
    └──────────┬──────┘    └──────────┬──────────────┘
               │                      │
    ┌──────────▼──────┐    ┌──────────▼──────────────┐
    │ AtmosphereResolver│  │  GraphQL Fetcher        │
    │ (time → mode)   │    │  (GitHub API / mock)    │
    └──────────┬──────┘    └──────────┬──────────────┘
               │                      │
    ┌──────────▼──────┐    ┌──────────▼──────────────┐
    │   ThemeLoader   │    │   CalendarGrid          │
    │ (JSON themes)   │    │   (grid mapping)        │
    └──────────┬──────┘    └──────────┬──────────────┘
               │                      │
    ┌──────────▼──────┐    ┌──────────▼──────────────┐
    │   Template      │    │   A* Pathfinder /       │
    │   Renderer      │    │   Timeline Planner      │
    └──────────┬──────┘    └──────────┬──────────────┘
               │                      │
    ┌──────────▼──────┐    ┌──────────▼──────────────┐
    │   README.md     │    │   SVG Compiler          │
    │   (output)      │    │   (cascading wave reset)│
    └─────────────────┘    └─────────────────────────┘
```

---

## Directory Structure

```
SAmarjeet05/
│
├── generate_readme.py          # CLI entry point
│
├── chronoai/                   # Core Python package
│   ├── __init__.py             # Version: v2.0.0
│   ├── builder.py              # READMEBuilder — main orchestrator
│   ├── theme.py                # Theme resolution and merging
│   ├── typing.py               # Typed configuration models
│   ├── stats.py                # GitHub stats URL builder
│   ├── footer.py               # README footer generator
│   │
│   ├── config/                 # Configuration loaders
│   ├── domain/                 # Domain models
│   ├── loaders/                # File/JSON loaders
│   ├── plugins/                # Pluggable section renderers
│   ├── renderers/              # Template rendering engine
│   ├── resolvers/              # AtmosphereResolver (time → mode)
│   ├── cache/                  # Hash-based cache system
│   │
│   └── motion/                 # ChronoMotion Engine (v2.0.0)
│       ├── models.py           # Shared data classes
│       ├── fetcher.py          # GraphQL API/Mock data fetcher
│       ├── grid.py             # Parses API data & coordinate layout
│       ├── planner.py          # A* path planner
│       ├── timeline.py         # Motion/Timing timeline planner
│       ├── palette.py          # Visual colors & atmospheres configs
│       ├── svg.py              # SVG compiler: waves, eye glow
│       └── renderer.py         # ChronoMotionRenderer orchestrator
│
├── themes/                     # Theme JSON files
│   ├── base.json               # Default fallback theme
│   ├── boot.json               # Boot atmosphere theme
│   ├── inference.json          # Inference atmosphere theme
│   ├── optimization.json       # Optimization atmosphere theme
│   └── research.json           # Research atmosphere theme
│
├── assets/                     # Static and generated assets
│   └── snake/                  # Generated contribution SVGs (8 files)
│       └── snake-{atmosphere}-{light|dark}.svg
│
├── cache/                      # Compiled README cache files
│   └── {mode}.md + {mode}.sha256
│
├── preview/                    # Preview copies of cached READMEs
├── generated/                  # Versioned copy of current README.md
├── tests/                      # Unit and integration tests
├── docs/                       # This documentation
└── .github/workflows/          # GitHub Actions
    └── update-profile.yml      # Single unified workflow
```

---

## Core Subsystems

| Subsystem | Module | Purpose |
|---|---|---|
| CLI | `generate_readme.py` | Entry point, argument parsing |
| README Builder | `chronoai/builder.py` | Orchestrates full README generation |
| Atmosphere Resolver | `chronoai/resolvers/` | Maps IST time → `boot/inference/optimization/research` |
| Theme Loader | `chronoai/theme.py` | Loads and merges JSON theme with base defaults |
| Plugins | `chronoai/plugins/` | Modular section renderers (skills, snake, stats…) |
| Cache | `chronoai/cache/` | SHA-256 hash-based README caching |
| ChronoMotion Engine | `chronoai/motion/` | Full native A* contribution loop + SMIL SVG engine |
| GitHub Actions | `.github/workflows/` | Automated scheduling and deployment |

---

## Design Principles

1. **Atmosphere-first**: All visual decisions (colors, animations, step kinetics) are driven by the current atmospheric mode.
2. **Fully self-contained**: No runtime dependencies on external services like Platane/snk.
3. **Separation of concerns**: Data parsing, A* path planning, timeline scheduling, and SVG rendering are strictly modular.
4. **Physically interactive**: Kinetic characteristics (such as AI thinking pause, Pac-Man overshoot, and cascading wave resets) simulate physical inertia.
5. **Cache-aware**: Expensively-rendered READMEs are cached and content-addressed with SHA-256.
