from __future__ import annotations


class StatsManager:
    @staticmethod
    def build_profile_stats_urls(context):
        """Build light and dark theme URLs for GitHub stats cards."""
        stats_config = context.theme.get("stats", {})
        username = context.config.username

        # Extract theme names from light/dark structure
        light_theme = "light"
        dark_theme = "dark"

        return {
            # GitHub Stats - build both light and dark
            "github_stats_light": (
                "https://github-readme-stats.vercel.app/api?"
                f"username={username}&show_icons=true&theme={light_theme}"
                "&hide_border=true&rank_icon=github"
            ),
            "github_stats_dark": (
                "https://github-readme-stats.vercel.app/api?"
                f"username={username}&show_icons=true&theme={dark_theme}"
                "&hide_border=true&rank_icon=github"
            ),
            # GitHub Streak - build both light and dark
            "streak_light": (
                "https://github-readme-streak-stats.herokuapp.com?"
                f"user={username}&theme={light_theme}&hide_border=true"
            ),
            "streak_dark": (
                "https://github-readme-streak-stats.herokuapp.com?"
                f"user={username}&theme={dark_theme}&hide_border=true"
            ),
            # Languages - build both light and dark
            "languages_light": (
                "https://github-readme-stats.vercel.app/api/top-langs/?"
                f"username={username}&layout=compact&theme={light_theme}"
                "&hide_border=true"
            ),
            "languages_dark": (
                "https://github-readme-stats.vercel.app/api/top-langs/?"
                f"username={username}&layout=compact&theme={dark_theme}"
                "&hide_border=true"
            ),
            # Activity Graph - build both light and dark
            "graph_light": (
                "https://github-readme-activity-graph.vercel.app/graph?"
                f"username={username}&theme={light_theme}&hide_border=true"
            ),
            "graph_dark": (
                "https://github-readme-activity-graph.vercel.app/graph?"
                f"username={username}&theme={dark_theme}&hide_border=true"
            ),
        }
