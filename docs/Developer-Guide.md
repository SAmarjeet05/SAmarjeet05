# Developer Guide

> ChronoAI v2.0.0 — Local Development & Contribution Reference

## Prerequisites

- Python 3.11+
- `git`
- (Optional) `GITHUB_TOKEN` for real contribution data

---

## Setup

```bash
# Clone the repository
git clone https://github.com/SAmarjeet05/SAmarjeet05.git
cd SAmarjeet05

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## Running Locally

```bash
# Generate README for the current atmosphere (cache-aware)
python generate_readme.py

# Force fresh generation (ignore cache)
python generate_readme.py --no-cache

# Test a specific atmosphere
python generate_readme.py --mode research

# Simulate a specific time of day
python generate_readme.py --time 22:30

# Print debug info
python generate_readme.py --debug

# Rebuild all caches and contribution SVGs
python generate_readme.py --build-cache

# Rebuild contribution SVGs only
python generate_readme.py --build-contribution
```

---

## Running Tests

```bash
# Run all unit tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run a specific test file
python -m pytest tests/test_snake_path.py -v
```

### Test Files

| File | What It Tests |
|---|---|
| `tests/test_atmosphere_resolver.py` | Atmosphere time window resolution |
| `tests/test_builtin_plugins.py` | Plugin section rendering |
| `tests/test_hash_cache.py` | SHA-256 cache read/write |
| `tests/test_schema_validator.py` | Theme JSON schema validation |
| `tests/test_snake_path.py` | A* pathfinding, timeline phases, and kinetics |

---

## Project Structure

See [Architecture.md](./Architecture.md) for the full directory layout.

---

## Adding a New Theme

1. Create `themes/{name}.json` (copy from an existing theme as a starting point)
2. Add `{name}` to the time windows in `chronoai/resolvers/atmosphere_resolver.py`
3. Add a `MotionPalette` for `{name}` in `chronoai/motion/palette.py`
4. Add a `"snake"` block in your theme JSON pointing to `assets/snake/snake-{name}-light.svg` etc.
5. Run `python generate_readme.py --build-cache` to generate and validate all outputs

---

## Adding a New Template Section

1. Add your `{{PLACEHOLDER}}` token to `README.template.md`
2. Create a plugin in `chronoai/plugins/` that returns the rendered Markdown for your section
3. Register it in `chronoai/builder.py`
4. Rebuild the cache

---

## Adding a New Animation (Future)

The engine is ready to support new animation types. To add one:

1. Create `chronoai/motion/animation/your_animator.py`
2. Implement custom motion kinetics or paths
3. Reference it from `palette.py` or `timeline.py`
4. Run `--build-contribution` to validate

---

## Code Style

- Python 3.11+ with `from __future__ import annotations`
- Type hints throughout
- `dataclasses` for data models
- `snake_case` for all identifiers
- No external runtime dependencies beyond `requirements.txt`

---

## Committing

```bash
git add .
git commit -m "feat: your change description"
git push
```

On push to `main`, the GitHub Actions workflow will automatically:
1. Rebuild all README caches and contribution SVGs (using real API data)
2. Generate the current atmosphere README
3. Commit and push all changed files
