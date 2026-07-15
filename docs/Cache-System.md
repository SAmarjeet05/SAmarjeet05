# Cache System

> ChronoAI v2.0.0 — Content-Addressed Caching Reference

## Overview

ChronoAI uses a **SHA-256 content-addressed cache** to avoid re-rendering identical READMEs. Since the rendered output for a given atmosphere only changes when the template, theme, or assets change, caching makes repeated scheduled runs near-instant.

---

## How It Works

```
Input:
  - README.template.md content
  - Merged theme JSON (base + atmosphere)
  - Current mode string

       ↓  SHA-256 hash

Computed Hash
       ↓
  Compare with cache/{mode}.sha256

  MATCH?
  ├── YES → Copy cache/{mode}.md → README.md (cache HIT)
  └── NO  → Render fresh → Write cache/{mode}.md + .sha256 (cache MISS)
```

---

## Cache Files

For each of the 4 atmosphere modes, two files are maintained:

| File | Content |
|---|---|
| `cache/{mode}.md` | Fully rendered README for this atmosphere |
| `cache/{mode}.sha256` | SHA-256 hash of the inputs that produced the cached README |

Example:
```
cache/
├── boot.md
├── boot.sha256
├── inference.md
├── inference.sha256
├── optimization.md
├── optimization.sha256
├── research.md
└── research.sha256
```

---

## Cache Hit Conditions

The cache is used if and only if:
1. `cache/{mode}.md` exists
2. `cache/{mode}.sha256` exists
3. The computed hash of the **current** inputs matches the stored hash

If any of these conditions fail, a fresh render is triggered.

---

## Bypassing the Cache

**Force a fresh render** for the current atmosphere:
```bash
python generate_readme.py --no-cache
```

**Rebuild all caches** for all four atmospheres at once:
```bash
python generate_readme.py --build-cache
```

This is typically run on `push` events in the GitHub Actions workflow, so that any template or theme change is immediately reflected in the caches.

---

## Preview Files

`--build-cache` also writes a parallel set of preview files:

```
preview/
├── boot.md
├── inference.md
├── optimization.md
└── research.md
```

These are identical to the cache files but are kept in a separate directory for easy human review without interfering with the cache system itself.

---

## Why Not Just Always Re-Render?

The scheduled workflow runs **4 times per day** — once at the start of each atmosphere window. On most days, only 2–3 of those runs need a new README (e.g., after midnight when the theme cycle resets). With caching:

- 60–80% of scheduled runs complete with a simple file copy
- Full re-renders only happen when template/theme/assets actually change
- The GitHub Actions log clearly shows `Cache: HIT` vs `Cache: MISS` for traceability

---

## Debug Output

When running with `--debug`, the cache status is shown in the formatted output:

```
═══════════════════════════════════════
ChronoAI Debug
═══════════════════════════════════════
Current Time (IST) : 20:05
Atmosphere         : Research
Theme File         : research.json
GitHub Theme       : Auto
Cache              : HIT
Generation Mode    : Cached
Output             : README.md
═══════════════════════════════════════
```
