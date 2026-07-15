import datetime
import os
import shutil
from chronoai.config.app import AppConfig
from chronoai.cache.hash_cache import HashCache
from chronoai.domain.context import BuildContext
from chronoai.resolvers.atmosphere_resolver import AtmosphereResolver
from chronoai.renderers.markdown_renderer import MarkdownRenderer
from chronoai.theme import ThemeLoader
from chronoai.typing import TypingManager
from chronoai.stats import StatsManager
from chronoai.footer import FooterManager
from chronoai.plugins.registry import PluginRegistry
from chronoai.plugins.builtins.profile_cards import BuiltinProfileCardsPlugin

class READMEBuilder:
    def __init__(self, template_path=None, themes_dir=None, cache_dir=None, preview_dir=None, config=None):
        self.config = config or AppConfig.default()
        self.template_path = template_path or self.config.template_path
        self.themes_dir = themes_dir or self.config.themes_dir
        self.cache_dir = cache_dir or self.config.cache_dir
        self.preview_dir = preview_dir or self.config.preview_dir
        self.theme_loader = ThemeLoader(self.themes_dir)
        self.renderer = MarkdownRenderer()
        self.plugins = PluginRegistry()
        if self.config.enable_builtin_plugins:
            self.plugins.register(BuiltinProfileCardsPlugin())

    def _build_context(self, mode, theme):
        utc_time = datetime.datetime.now(datetime.timezone.utc)
        local_time = AtmosphereResolver.local_now(self.config.timezone_name)
        return BuildContext(
            config=self.config,
            mode=mode,
            theme=theme,
            current_time_utc=utc_time,
            current_time_local=local_time,
        )

    def get_current_mode(self):
        return AtmosphereResolver.resolve_mode(AtmosphereResolver.local_now(self.config.timezone_name))

    def build(self, force_mode=None, use_cache=True):
        mode = force_mode if force_mode else self.get_current_mode()
        print(f"Resolving build for mode: '{mode}' (use_cache={use_cache})")

        cache_file = os.path.join(self.cache_dir, f"{mode}.md")
        hash_file = os.path.join(self.cache_dir, f"{mode}.sha256")

        if use_cache:
            if os.path.exists(cache_file):
                print(f"Cache hit! Copying pre-built cache from {cache_file}")
                self._write_readme_files_from_source(cache_file)
                return True
            else:
                print(f"Cache miss! Pre-built cache not found at {cache_file}. Proceeding with fresh build.")

        # Perform fresh dynamic build
        readme_content = self.generate_content(mode)
        digest = HashCache.compute(readme_content)
        previous_digest = HashCache.read(hash_file)

        if previous_digest == digest and os.path.exists(cache_file):
            print(f"Hash unchanged for mode '{mode}'. Reusing cached README content.")
            self._write_readme_files_from_source(cache_file)
            return True
        
        # Write files
        self._write_readme_files(readme_content)
        
        # Update cache file with this latest dynamic render
        os.makedirs(self.cache_dir, exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"Updated cache file at {cache_file}")

        HashCache.write(hash_file, digest)

        if previous_digest == digest:
            print(f"Hash unchanged for mode '{mode}'. Cache content is stable.")
        else:
            print(f"Updated hash cache at {hash_file}")
        return False

    def generate_content(self, mode, shuffle_typing=True):
        theme = self.theme_loader.load(mode)
        context = self._build_context(mode, theme)
        
        banner_path = theme.get("banner", "")
        divider_path = theme.get("divider_path", "")
        mode_name = theme.get("mode", "")

        typing_url = TypingManager.build_typing_url(context, shuffle=shuffle_typing)
        stats_urls = StatsManager.build_profile_stats_urls(context)
        quote = FooterManager.build_footer(context)
        status_picture = self._build_picture(
            light_src=theme.status_light,
            dark_src=theme.status_dark,
            alt_text="AI System Status",
            width="280px",
            centered=True,
        )
        snake_picture = self._build_picture(
            light_src=theme.snake_light,
            dark_src=theme.snake_dark,
            alt_text="Snake animation",
            width="100%",
        )
        # Build picture elements for stats (light/dark theme-aware)
        github_stats_picture = self._build_picture(
            light_src=stats_urls["github_stats_light"],
            dark_src=stats_urls["github_stats_dark"],
            alt_text="GitHub Stats",
            width="48%",
        )
        streak_picture = self._build_picture(
            light_src=stats_urls["streak_light"],
            dark_src=stats_urls["streak_dark"],
            alt_text="GitHub Streak",
            width="48%",
        )
        languages_picture = self._build_picture(
            light_src=stats_urls["languages_light"],
            dark_src=stats_urls["languages_dark"],
            alt_text="Top Languages",
            width="48%",
        )
        graph_picture = self._build_picture(
            light_src=stats_urls["graph_light"],
            dark_src=stats_urls["graph_dark"],
            alt_text="GitHub Activity Graph",
            width="48%",
        )
        
        # Load template
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template file not found at {self.template_path}")
            
        with open(self.template_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        replacements = {
            "{{BANNER_PATH}}": banner_path,
            "{{STATUS_PICTURE}}": status_picture,
            "{{DIVIDER_PATH}}": divider_path,
            "{{MODE_NAME}}": mode_name,
            "{{TYPING_URL}}": typing_url,
            "{{GITHUB_STATS}}": github_stats_picture,
            "{{STREAK}}": streak_picture,
            "{{LANGUAGES}}": languages_picture,
            "{{GRAPH}}": graph_picture,
            "{{SNAKE_PICTURE}}": snake_picture,
            "{{FOOTER_QUOTE}}": quote
        }
        
        content = self.renderer.render(content, replacements)
        plugin_markup = self.plugins.render_all(context)
        content = content.replace("{{PLUGINS}}", plugin_markup)
            
        # Append metadata version comment at bottom
        theme_version = theme.get("version", "1.0")
        meta_comment = FooterManager.generate_metadata_comment(mode, theme_version)
        content = f"{content}\n\n{meta_comment}\n"
        
        return content

    def build_all_caches(self):
        """Compiles and updates caches and preview files for all 4 modes."""
        modes = list(self.config.build_modes)
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.preview_dir, exist_ok=True)
        
        print("Compiling caches and preview files for all operational modes...")
        for m in modes:
            # Generate content (keep typing shuffle active for variety in cache)
            content = self.generate_content(m, shuffle_typing=True)
            digest = HashCache.compute(content)
            
            # Save to cache
            cache_path = os.path.join(self.cache_dir, f"{m}.md")
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f" -> Compiled cache: {cache_path}")

            hash_path = os.path.join(self.cache_dir, f"{m}.sha256")
            HashCache.write(hash_path, digest)
            print(f" -> Updated hash cache: {hash_path}")
            
            # Save to preview
            preview_path = os.path.join(self.preview_dir, f"{m}.md")
            with open(preview_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f" -> Generated preview: {preview_path}")
            
        print("All caches and previews successfully compiled!")

    def _write_readme_files(self, content):
        # Write to root README.md
        with open(self.config.root_readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully generated root {self.config.root_readme_path}")

        # Also write to generated/README.md
        os.makedirs("generated", exist_ok=True)
        with open(self.config.generated_readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully generated {self.config.generated_readme_path}")

    def _write_readme_files_from_source(self, source_path):
        # Copy to root README.md
        shutil.copy(source_path, self.config.root_readme_path)
        print(f"Successfully copied to root {self.config.root_readme_path}")

        # Copy to generated/README.md
        os.makedirs("generated", exist_ok=True)
        shutil.copy(source_path, self.config.generated_readme_path)
        print(f"Successfully copied to {self.config.generated_readme_path}")

    def _build_picture(self, light_src, dark_src, alt_text, width="100%", centered=False):
        light_src = light_src or dark_src
        dark_src = dark_src or light_src
        style = "display: block; margin: 0 auto;" if centered else ""
        style_attr = f" style='{style}'" if style else ""
        return (
            "<picture>"
            f"<source media='(prefers-color-scheme: dark)' srcset='{dark_src}' />"
            f"<source media='(prefers-color-scheme: light)' srcset='{light_src}' />"
            f"<img src='{light_src}' alt='{alt_text}' width='{width}'{style_attr} />"
            "</picture>"
        )
