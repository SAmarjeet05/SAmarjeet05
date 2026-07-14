from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class PluginRegistry:
    plugins: list[object] = field(default_factory=list)

    def register(self, plugin: object) -> None:
        self.plugins.append(plugin)

    def extend(self, plugins: Iterable[object]) -> None:
        for plugin in plugins:
            self.register(plugin)

    def render_all(self, context) -> str:
        fragments: list[str] = []
        for plugin in self.plugins:
            render = getattr(plugin, "render", None)
            if callable(render):
                fragment = render(context)
                if fragment:
                    fragments.append(fragment)
        return "\n\n".join(fragments)