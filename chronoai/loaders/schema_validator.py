from __future__ import annotations


class ThemeSchemaError(ValueError):
    pass


class ThemeSchemaValidator:
    REQUIRED_TOP_LEVEL_KEYS = {"typing", "footer", "quotes"}

    @classmethod
    def validate(cls, mapping: dict) -> None:
        missing = sorted(key for key in cls.REQUIRED_TOP_LEVEL_KEYS if key not in mapping)
        if missing:
            raise ThemeSchemaError(f"Theme is missing required keys: {', '.join(missing)}")

        typing = mapping.get("typing", {})
        if not isinstance(typing, dict):
            raise ThemeSchemaError("Theme key 'typing' must be an object")

        footer = mapping.get("footer", {})
        if not isinstance(footer, dict):
            raise ThemeSchemaError("Theme key 'footer' must be an object")

        quotes = mapping.get("quotes", [])
        if not isinstance(quotes, list):
            raise ThemeSchemaError("Theme key 'quotes' must be a list")

        for key in ("stats", "graph", "snake"):
            if key not in mapping:
                continue
            value = mapping.get(key, {})
            if not isinstance(value, dict):
                raise ThemeSchemaError(f"Theme key '{key}' must be an object")