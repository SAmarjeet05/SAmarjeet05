# Contributing to ChronoAI

## Development setup

1. Create and activate a virtual environment.
2. Install dependencies if needed.
3. Run README generation:

   python generate_readme.py

## Running tests

Run the built-in test suite:

   python -m unittest discover -s tests -p "test_*.py"

## Architecture overview

- config: application configuration only
- domain: typed models and context
- loaders: theme loading and validation
- resolvers: pure decision logic like atmosphere resolution
- renderers: markdown rendering only
- cache: hash helpers
- plugins: extension points and optional modules

## Theme authoring guidance

Use structured theme keys as described in docs/theme-schema.md.
Keep atmosphere data independent from GitHub light and dark presentation.
