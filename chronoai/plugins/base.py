from __future__ import annotations

from typing import Protocol


class BuildPlugin(Protocol):
    name: str

    def render(self, context) -> str:
        """Return markdown content for this plugin."""
        raise NotImplementedError