from __future__ import annotations


class StatsManager:
    @staticmethod
    def get_stats_theme(stats_config):
        return stats_config.get("github", "default")

    @staticmethod
    def get_streak_theme(stats_config):
        return stats_config.get("streak", "default")

    @staticmethod
    def get_activity_theme(stats_config):
        return stats_config.get("graph", "github")

    @staticmethod
    def get_snake_svg(stats_config):
        return stats_config.get("graph", "github-contribution-grid-snake.svg")

    @staticmethod
    def build_profile_stats_urls(context):
        stats_config = context.theme.get("stats", {})
        username = context.config.username

        return {
            "github_stats": (
                "https://github-readme-stats.vercel.app/api?"
                f"username={username}&show_icons=true&theme={StatsManager.get_stats_theme(stats_config)}"
                "&hide_border=true&rank_icon=github"
            ),
            "streak": (
                "https://github-readme-streak-stats.herokuapp.com?"
                f"user={username}&theme={StatsManager.get_streak_theme(stats_config)}&hide_border=true"
            ),
            "languages": (
                "https://github-readme-stats.vercel.app/api/top-langs/?"
                f"username={username}&layout=compact&theme={StatsManager.get_stats_theme(stats_config)}"
                "&hide_border=true"
            ),
            "graph": (
                "https://github-readme-activity-graph.vercel.app/graph?"
                f"username={username}&theme={StatsManager.get_activity_theme(stats_config)}&hide_border=true"
            ),
        }
