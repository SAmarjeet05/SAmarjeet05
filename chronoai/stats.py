from __future__ import annotations


class StatsManager:
    @staticmethod
    def build_profile_stats_urls(context):
        """Build light and dark theme URLs for GitHub stats cards."""
        stats_config = context.theme.get("stats", {})
        username = context.config.username

        light_config = stats_config.get("light", {})
        dark_config = stats_config.get("dark", {})

        def get_colors_query(cfg):
            if not cfg:
                return ""
            params = []
            for param_name in ("bg_color", "title_color", "text_color", "icon_color", "border_color"):
                if param_name in cfg:
                    params.append(f"{param_name}={cfg[param_name]}")
            return "&" + "&".join(params) if params else ""

        def get_streak_colors_query(cfg):
            if not cfg:
                return ""
            params = []
            if "bg_color" in cfg:
                params.append(f"background={cfg['bg_color']}")
            if "border_color" in cfg:
                params.append(f"border={cfg['border_color']}")
                params.append(f"stroke={cfg['border_color']}")
            if "icon_color" in cfg:
                params.append(f"ring={cfg['icon_color']}")
                params.append(f"fire={cfg['icon_color']}")
            if "title_color" in cfg:
                params.append(f"currStreakNum={cfg['title_color']}")
            if "text_color" in cfg:
                params.append(f"sideNums={cfg['text_color']}")
                params.append(f"sideLabels={cfg['text_color']}")
                params.append(f"currStreakLabel={cfg['text_color']}")
                params.append(f"dates={cfg['text_color']}")
            return "&" + "&".join(params) if params else ""

        def get_graph_colors_query(cfg):
            if not cfg:
                return ""
            params = []
            if "bg_color" in cfg:
                params.append(f"bg_color={cfg['bg_color']}")
            if "text_color" in cfg:
                params.append(f"color={cfg['text_color']}")
            if "title_color" in cfg:
                params.append(f"title_color={cfg['title_color']}")
            if "icon_color" in cfg:
                params.append(f"line={cfg['icon_color']}")
                params.append(f"point={cfg['icon_color']}")
            return "&" + "&".join(params) if params else ""

        light_query = get_colors_query(light_config)
        dark_query = get_colors_query(dark_config)

        light_streak_query = get_streak_colors_query(light_config)
        dark_streak_query = get_streak_colors_query(dark_config)

        light_graph_query = get_graph_colors_query(light_config)
        dark_graph_query = get_graph_colors_query(dark_config)

        # Predefined themes to start with
        light_theme = "light"
        dark_theme = "dark"

        return {
            # GitHub Stats - build both light and dark
            "github_stats_light": (
                "https://github-readme-stats.vercel.app/api?"
                f"username={username}&show_icons=true&theme={light_theme}"
                f"&hide_border=true&rank_icon=github{light_query}"
            ),
            "github_stats_dark": (
                "https://github-readme-stats.vercel.app/api?"
                f"username={username}&show_icons=true&theme={dark_theme}"
                f"&hide_border=true&rank_icon=github{dark_query}"
            ),
            # GitHub Streak - build both light and dark
            "streak_light": (
                "https://streak-stats.demolab.com?"
                f"user={username}&theme={light_theme}&hide_border=true{light_streak_query}"
            ),
            "streak_dark": (
                "https://streak-stats.demolab.com?"
                f"user={username}&theme={dark_theme}&hide_border=true{dark_streak_query}"
            ),
            # Languages - build both light and dark
            "languages_light": (
                "https://github-readme-stats.vercel.app/api/top-langs/?"
                f"username={username}&layout=compact&theme={light_theme}"
                f"&hide_border=true{light_query}"
            ),
            "languages_dark": (
                "https://github-readme-stats.vercel.app/api/top-langs/?"
                f"username={username}&layout=compact&theme={dark_theme}"
                f"&hide_border=true{dark_query}"
            ),
            # Activity Graph - build both light and dark
            "graph_light": (
                "https://github-readme-activity-graph.vercel.app/graph?"
                f"username={username}&theme={light_theme}&hide_border=true{light_graph_query}"
            ),
            "graph_dark": (
                "https://github-readme-activity-graph.vercel.app/graph?"
                f"username={username}&theme={dark_theme}&hide_border=true{dark_graph_query}"
            ),
        }
