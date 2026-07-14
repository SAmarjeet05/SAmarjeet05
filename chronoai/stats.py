class StatsManager:
    @staticmethod
    def get_stats_theme(stats_config):
        return stats_config.get("github", "default")

    @staticmethod
    def get_streak_theme(stats_config):
        return stats_config.get("streak", "default")

    @staticmethod
    def get_snake_svg(stats_config):
        return stats_config.get("graph", "github-contribution-grid-snake.svg")
