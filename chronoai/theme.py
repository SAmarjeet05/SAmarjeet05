import json
import os

from chronoai.loaders.schema_validator import ThemeSchemaValidator
from chronoai.domain.theme import Theme


class ThemeLoader:
    def __init__(self, themes_dir="themes"):
        self.themes_dir = themes_dir

    def load(self, name):
        """Loads, resolves inheritance, and normalizes a theme."""
        theme_path = os.path.join(self.themes_dir, f"{name}.json")
        if not os.path.exists(theme_path):
            raise FileNotFoundError(f"Theme '{name}' not found at {theme_path}")

        theme_data = self._load_raw(theme_path)

        if "extends" in theme_data:
            parent_name = theme_data["extends"]
            parent_data = self._load_by_name(parent_name)
            theme_data = self._merge_dicts(parent_data, theme_data)

        ThemeSchemaValidator.validate(theme_data)

        return Theme.from_mapping(name=name, mapping=theme_data, source_path=theme_path)

    def _load_by_name(self, name):
        theme_path = os.path.join(self.themes_dir, f"{name}.json")
        if not os.path.exists(theme_path):
            raise FileNotFoundError(f"Theme '{name}' not found at {theme_path}")
        return self._load_raw(theme_path)

    def _load_raw(self, theme_path):
        with open(theme_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _merge_dicts(self, dict1, dict2):
        """Recursively merges dict2 into dict1."""
        merged = dict1.copy()
        for key, value in dict2.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_dicts(merged[key], value)
            else:
                merged[key] = value
        return merged
