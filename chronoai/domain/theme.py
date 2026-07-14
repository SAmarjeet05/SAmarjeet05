from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ThemeAssets:
    banner: str = ""
    divider: str = ""
    status_light: str = ""
    status_dark: str = ""
    snake_light: str = ""
    snake_dark: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            "banner": self.banner,
            "divider": self.divider,
            "status_light": self.status_light,
            "status_dark": self.status_dark,
            "snake_light": self.snake_light,
            "snake_dark": self.snake_dark,
        }


@dataclass(frozen=True)
class Theme:
    name: str
    version: str = "1.0"
    mode: str = ""
    source_path: str = ""
    assets: ThemeAssets = field(default_factory=ThemeAssets)
    typing: dict[str, Any] = field(default_factory=dict)
    footer: dict[str, Any] = field(default_factory=dict)
    stats: dict[str, Any] = field(default_factory=dict)
    snake: dict[str, Any] = field(default_factory=dict)
    quotes: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_mapping(cls, name: str, mapping: dict[str, Any], source_path: str = "") -> "Theme":
        """Create Theme from normalized JSON structure (with assets/status/snake nesting)."""
        assets_section = dict(mapping.get("assets", {}))
        status_section = dict(assets_section.get("status", {}))
        snake_section = dict(mapping.get("snake", {}))

        assets = ThemeAssets(
            banner=assets_section.get("banner", ""),
            divider=assets_section.get("divider", ""),
            status_light=status_section.get("light", ""),
            status_dark=status_section.get("dark", ""),
            snake_light=snake_section.get("light", ""),
            snake_dark=snake_section.get("dark", ""),
        )

        return cls(
            name=name,
            version=str(mapping.get("version", "1.0")),
            mode=str(mapping.get("mode", "")),
            source_path=source_path,
            assets=assets,
            typing=dict(mapping.get("typing", {})),
            footer=dict(mapping.get("footer", {})),
            stats=dict(mapping.get("stats", {})),
            snake=dict(mapping.get("snake", {})),
            quotes=tuple(mapping.get("quotes", [])),
            metadata={
                key: value
                for key, value in mapping.items()
                if key not in {"assets", "typing", "footer", "stats", "snake", "quotes", "version", "mode"}
            },
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Dict-like access for compatibility with service managers."""
        lookup = {
            "name": self.name,
            "version": self.version,
            "mode": self.mode,
            "banner": self.assets.banner,
            "divider": self.assets.divider,
            "status_light": self.assets.status_light,
            "status_dark": self.assets.status_dark,
            "snake_light": self.assets.snake_light,
            "snake_dark": self.assets.snake_dark,
            "assets": self.assets.as_dict(),
            "typing": self.typing,
            "footer": self.footer,
            "stats": self.stats,
            "snake": self.snake,
            "quotes": list(self.quotes),
        }
        if key in lookup:
            return lookup[key]
        return self.metadata.get(key, default)

    @property
    def status_light(self) -> str:
        """Normalized status light SVG path from assets."""
        return self.assets.status_light

    @property
    def status_dark(self) -> str:
        """Normalized status dark SVG path from assets."""
        return self.assets.status_dark

    @property
    def snake_light(self) -> str:
        """Normalized snake light SVG path from assets."""
        return self.assets.snake_light

    @property
    def snake_dark(self) -> str:
        """Normalized snake dark SVG path from assets."""
        return self.assets.snake_dark

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "mode": self.mode,
            "assets": self.assets.as_dict(),
            "typing": dict(self.typing),
            "footer": dict(self.footer),
            "stats": dict(self.stats),
            "snake": dict(self.snake),
            "quotes": list(self.quotes),
            **self.metadata,
        }