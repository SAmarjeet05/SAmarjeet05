# ChronoAI Theme Schema

This document describes the recommended theme structure for atmosphere files in the themes folder.

## Required shared keys

All themes, including base, should provide:

- typing: object
- footer: object
- quotes: array

## Atmosphere keys

Operational atmosphere themes are expected to provide:

- mode: string
- assets.banner: path
- assets.divider: path
- assets.status.light: path
- assets.status.dark: path
- snake.light: path
- snake.dark: path
- stats: object
- graph: object

## Backward compatibility

Legacy key names are still accepted by the loader for compatibility:

- banner
- divider_path
- status_svg
- status_light
- status_dark
- snake_svg
- snake_light
- snake_dark

Use structured keys for new themes.
