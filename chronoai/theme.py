import json
import os

class ThemeLoader:
    def __init__(self, themes_dir="themes"):
        self.themes_dir = themes_dir

    def load(self, name):
        """Loads and resolves inheritance for a theme."""
        theme_path = os.path.join(self.themes_dir, f"{name}.json")
        if not os.path.exists(theme_path):
            raise FileNotFoundError(f"Theme '{name}' not found at {theme_path}")

        with open(theme_path, "r", encoding="utf-8") as f:
            theme_data = json.load(f)

        # Handle extends recursively
        if "extends" in theme_data:
            parent_name = theme_data["extends"]
            parent_data = self.load(parent_name)
            
            # Perform deep merge
            theme_data = self._merge_dicts(parent_data, theme_data)
            
        return theme_data

    def _merge_dicts(self, dict1, dict2):
        """Recursively merges dict2 into dict1."""
        merged = dict1.copy()
        for key, value in dict2.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_dicts(merged[key], value)
            else:
                merged[key] = value
        return merged
