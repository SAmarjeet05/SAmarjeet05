import datetime
import os
import shutil
from chronoai.theme import ThemeLoader
from chronoai.typing import TypingManager
from chronoai.stats import StatsManager
from chronoai.footer import FooterManager

class READMEBuilder:
    def __init__(self, template_path="README.template.md", themes_dir="themes", cache_dir="cache", preview_dir="preview"):
        self.template_path = template_path
        self.themes_dir = themes_dir
        self.cache_dir = cache_dir
        self.preview_dir = preview_dir
        self.theme_loader = ThemeLoader(themes_dir)

    def get_current_mode(self):
        # Current local time in IST (UTC+5:30)
        utc_time = datetime.datetime.now(datetime.timezone.utc)
        ist_time = utc_time + datetime.timedelta(hours=5, minutes=30)
        hour = ist_time.hour
        
        if 6 <= hour < 12:
            return "boot"
        elif 12 <= hour < 18:
            return "inference"
        elif 18 <= hour < 22:
            return "optimization"
        else:
            return "research"

    def build(self, force_mode=None, use_cache=False):
        mode = force_mode if force_mode else self.get_current_mode()
        print(f"Resolving build for mode: '{mode}' (use_cache={use_cache})")

        if use_cache:
            cache_file = os.path.join(self.cache_dir, f"{mode}.md")
            if os.path.exists(cache_file):
                print(f"Cache hit! Copying pre-built cache from {cache_file}")
                self._write_readme_files_from_source(cache_file)
                return
            else:
                print(f"Cache miss! Pre-built cache not found at {cache_file}. Proceeding with fresh build.")

        # Perform fresh dynamic build
        readme_content = self.generate_content(mode)
        
        # Write files
        self._write_readme_files(readme_content)
        
        # Update cache file with this latest dynamic render
        os.makedirs(self.cache_dir, exist_ok=True)
        cache_path = os.path.join(self.cache_dir, f"{mode}.md")
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"Updated cache file at {cache_path}")

    def generate_content(self, mode, shuffle_typing=True):
        theme = self.theme_loader.load(mode)
        
        # Resolve variables using managers
        banner_path = theme.get("banner", "")
        status_path = theme.get("status_svg", "")
        divider_path = theme.get("divider_path", "")
        mode_name = theme.get("mode", "")
        
        typing_config = theme.get("typing", {})
        typing_color = TypingManager.get_color(typing_config)
        typing_lines = TypingManager.get_lines_query(typing_config, shuffle=shuffle_typing)
        
        stats_config = theme.get("stats", {})
        stats_theme = StatsManager.get_stats_theme(stats_config)
        streak_theme = StatsManager.get_streak_theme(stats_config)
        snake_svg = StatsManager.get_snake_svg(stats_config)
        
        quote = FooterManager.get_random_quote(theme)
        
        # Load template
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template file not found at {self.template_path}")
            
        with open(self.template_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace variables
        replacements = {
            "{{BANNER_PATH}}": banner_path,
            "{{STATUS_PATH}}": status_path,
            "{{DIVIDER_PATH}}": divider_path,
            "{{MODE_NAME}}": mode_name,
            "{{TYPING_COLOR}}": typing_color,
            "{{TYPING_LINES}}": typing_lines,
            "{{STATS_THEME}}": stats_theme,
            "{{STREAK_THEME}}": streak_theme,
            "{{SNAKE_SVG}}": snake_svg,
            "{{FOOTER_QUOTE}}": quote
        }
        
        for key, value in replacements.items():
            content = content.replace(key, value)
            
        # Append metadata version comment at bottom
        theme_version = theme.get("version", "1.0")
        meta_comment = FooterManager.generate_metadata_comment(mode, theme_version)
        content = f"{content}\n\n{meta_comment}\n"
        
        return content

    def build_all_caches(self):
        """Compiles and updates caches and preview files for all 4 modes."""
        modes = ["boot", "inference", "optimization", "research"]
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.preview_dir, exist_ok=True)
        
        print("Compiling caches and preview files for all operational modes...")
        for m in modes:
            # Generate content (keep typing shuffle active for variety in cache)
            content = self.generate_content(m, shuffle_typing=True)
            
            # Save to cache
            cache_path = os.path.join(self.cache_dir, f"{m}.md")
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f" -> Compiled cache: {cache_path}")
            
            # Save to preview
            preview_path = os.path.join(self.preview_dir, f"{m}.md")
            with open(preview_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f" -> Generated preview: {preview_path}")
            
        print("All caches and previews successfully compiled!")

    def _write_readme_files(self, content):
        # Write to root README.md
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)
        print("Successfully generated root README.md")

        # Also write to generated/README.md
        os.makedirs("generated", exist_ok=True)
        with open(os.path.join("generated", "README.md"), "w", encoding="utf-8") as f:
            f.write(content)
        print("Successfully generated generated/README.md")

    def _write_readme_files_from_source(self, source_path):
        # Copy to root README.md
        shutil.copy(source_path, "README.md")
        print("Successfully copied to root README.md")

        # Copy to generated/README.md
        os.makedirs("generated", exist_ok=True)
        shutil.copy(source_path, os.path.join("generated", "README.md"))
        print("Successfully copied to generated/README.md")
