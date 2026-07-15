# GitHub Actions

> ChronoAI v2.0.0 — Automation & Workflow Reference

## Overview

ChronoAI uses a **single unified GitHub Actions workflow** (`update-profile.yml`) to handle all automation. The external `Platane/snk` snake workflow has been completely removed — all SVG generation is handled natively by the ChronoMotion Engine.

---

## Workflow File

**Location:** `.github/workflows/update-profile.yml`

---

## Trigger Events

### 1. Scheduled (`cron`)
Runs automatically at the start of each atmosphere window (IST → UTC):

| IST Time | UTC Cron | Atmosphere |
|---|---|---|
| 00:30 IST | `30 0 * * *` | Boot |
| 06:30 IST | `0 1 * * *` (approx) | Inference |
| 12:00 UTC | `0 12 * * *` | Optimization |
| 16:00 UTC | `0 16 * * *` | Research |

Exact cron expressions from the workflow:
```yaml
- cron: "30 0,5 * * *"
- cron: "0 12,16 * * *"
```

### 2. Push to `main`
Triggered when any of these paths change:

```yaml
paths:
  - "README.template.md"
  - "generate_readme.py"
  - "chronoai/**"
  - "themes/**"
  - "assets/**"
  - "tests/**"
```

On push, the workflow **rebuilds all caches and contribution SVGs** from scratch to ensure consistency.

### 3. Manual (`workflow_dispatch`)
Can be triggered manually from the GitHub Actions UI, with an optional input:

| Input | Type | Default | Description |
|---|---|---|---|
| `use_cache` | boolean | `true` | Whether to use cached README or force fresh render |

---

## Workflow Steps

```
Checkout → Setup Python → Install deps → Build cache (push only) → Generate README → Commit
```

### Step 1: Checkout
```yaml
- uses: actions/checkout@v4
```

### Step 2: Setup Python 3.12
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Compile Cache + Contribution SVGs (push only)
```bash
python generate_readme.py --build-cache
```
Runs `--build-cache` which:
- Rebuilds README caches for all 4 atmospheres
- Regenerates all 8 contribution SVGs using the real GitHub GraphQL API (via `GITHUB_TOKEN`)

**Environment:**
```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Step 5: Generate README
```bash
# Scheduled / manual with use_cache=true:
python generate_readme.py --debug

# Manual with use_cache=false:
python generate_readme.py --debug --no-cache
```

This resolves the current atmosphere from IST time and generates `README.md`.

### Step 6: Commit and Push
```bash
git add .
git diff --cached --quiet || git commit -m "chore: update ChronoAI profile" && git push
```

Only commits if there are actual changes — prevents empty commits on cache hits.

---

## Required Secrets

| Secret | Source | Description |
|---|---|---|
| `GITHUB_TOKEN` | Auto-provided by Actions | Required for GraphQL API and push permissions |

No additional secrets or personal access tokens are required.

---

## Permissions

The workflow uses minimal permissions:
```yaml
permissions:
  contents: write
```

Only `contents: write` is needed to push the updated README and SVGs.

---

## Removed Workflow: `snake.yml`

The previous workflow `snake.yml` used `Platane/snk/svg-only@v3` to generate the contribution snake SVG via an external GitHub Action and committed to an `output` branch.

This has been **completely replaced** by the native ChronoMotion Engine. Benefits:
- ✅ No dependency on `Platane/snk`
- ✅ Atmosphere-themed SVGs (8 variants) instead of 2 generic ones
- ✅ No separate `output` branch needed
- ✅ SVGs committed directly to `assets/snake/` in `main`
- ✅ Single workflow instead of two
