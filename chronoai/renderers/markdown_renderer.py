from __future__ import annotations


class MarkdownRenderer:
    def render(self, template: str, replacements: dict[str, str]) -> str:
        rendered = template
        for key, value in replacements.items():
            rendered = rendered.replace(key, value)
        return rendered