from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    username: str = "SAmarjeet05"
    timezone_name: str = "Asia/Kolkata"
    template_path: str = "README.template.md"
    themes_dir: str = "themes"
    cache_dir: str = "cache"
    preview_dir: str = "preview"
    root_readme_path: str = "README.md"
    generated_readme_path: str = "generated/README.md"
    output_repo_path: str = "output"
    shuffle_typing_lines: bool = True
    build_modes: tuple[str, ...] = ("boot", "inference", "optimization", "research")
    enable_builtin_plugins: bool = True
    spotify_now_playing_url: str = ""
    leetcode_card_url: str = ""
    blog_feed_url: str = ""
    weather_card_url: str = ""

    @classmethod
    def default(cls) -> "AppConfig":
        return cls()