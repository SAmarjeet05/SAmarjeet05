# Theme System

> ChronoAI v2.0.0 — Theme Architecture Reference

## Overview

ChronoAI uses a **layered JSON theme system**. Every visual output — README colors, contribution calendar palettes, stats card colors, dividers, and snake animations — is driven entirely by theme configuration. No color values are hardcoded in application code.

---

## Atmosphere Modes

The system operates in four **atmosphere modes**, automatically resolved from the current IST time:

| Mode | IST Window | Visual Identity |
|---|---|---|
| `boot` | 00:00 – 06:00 | Deep blue, cool slate, minimal |
| `inference` | 06:00 – 11:00 | Electric cyan, high contrast |
| `optimization` | 11:00 – 17:30 | Warm amber, earthy tones |
| `research` | 17:30 – 00:00 | Rich purple, deep violet |

---

## Theme File Format

Each atmosphere has a JSON theme file in `themes/`:

```json
{
  "meta": {
    "name": "Optimization",
    "version": "2.0"
  },
  "typing": {
    "font": "Fira Code",
    "color": "d08770",
    "lines": ["Scaling Intelligence", "Optimizing AI Systems"]
  },
  "stats": {
    "light": {
      "bg_color": "FFFDF9",
      "title_color": "3B2F2F",
      "text_color": "6B5A50",
      "icon_color": "D08770",
      "border_color": "F3DFC9"
    },
    "dark": {
      "bg_color": "17120F",
      "title_color": "F9F5F0",
      "text_color": "D8C8B8",
      "icon_color": "F4A261",
      "border_color": "5A3C2E"
    }
  },
  "snake": {
    "light": "assets/snake/snake-optimization-light.svg",
    "dark": "assets/snake/snake-optimization-dark.svg"
  }
}
```

---

## Base Theme & Inheritance

`themes/base.json` defines global defaults for all fields. Individual theme files only need to override what they change. At build time, the theme loader deep-merges the active theme on top of `base.json`:

```
base.json (defaults)
     +
optimization.json (overrides)
     ↓
Merged Theme Object
```

This means a theme only needs to declare fields that differ from the base.

---

## Theme Fields Reference

### `meta`
| Field | Type | Description |
|---|---|---|
| `name` | string | Human-readable theme name |
| `version` | string | Schema version |

### `typing`
Controls the animated typing SVG banner.

| Field | Type | Description |
|---|---|---|
| `font` | string | Font family name (e.g. `"Fira Code"`) |
| `color` | string | Hex color (no `#`) for the typing text |
| `lines` | array | List of strings to cycle through |

### `stats`
Controls GitHub stats/streak/graph card URL color parameters. Split into `light` and `dark` sub-objects.

| Field | Description |
|---|---|
| `bg_color` | Card background color (hex, no `#`) |
| `title_color` | Card title text color |
| `text_color` | Card body text color |
| `icon_color` | Icon / accent color |
| `border_color` | Card border color |

### `snake`
Paths to the pre-generated contribution calendar SVGs for this atmosphere.

| Field | Description |
|---|---|
| `light` | Relative path to the light-mode SVG |
| `dark` | Relative path to the dark-mode SVG |

---

## ChronoMotion Engine Palettes

The ChronoMotion Engine uses a parallel palette system defined in `chronoai/motion/palette.py`. Each atmosphere defines a `MotionPalette`:

```python
@dataclass(frozen=True)
class MotionPalette:
    bg: str
    empty: str
    snake: str
    levels: tuple[str, str, str, str, str]  # 0=empty, 1=Q1, 2=Q2, 3=Q3, 4=Q4
    text: str
    glow_color: str
```

These palettes are **separate** from the stats theme because the SVG renderer needs a different color model (it controls every pixel itself, rather than passing URL parameters to an external service).

---

## Adding a New Theme

1. Create `themes/{name}.json` with your overrides.
2. Add `{name}` to `AtmosphereResolver` time windows in `chronoai/resolvers/`.
3. Add a corresponding `AtmospherePalette` entry in `chronoai/contribution/palette.py`.
4. Add a snake block pointing to `assets/snake/snake-{name}-light.svg` and `assets/snake/snake-{name}-dark.svg`.
5. Run `python generate_readme.py --build-cache` to generate all outputs.
