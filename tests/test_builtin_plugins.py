import unittest
from datetime import datetime, timezone

from chronoai.config.app import AppConfig
from chronoai.domain.context import BuildContext
from chronoai.domain.theme import Theme
from chronoai.plugins.builtins.profile_cards import BuiltinProfileCardsPlugin


class BuiltinPluginTests(unittest.TestCase):
    def test_no_config_renders_empty(self):
        plugin = BuiltinProfileCardsPlugin()
        context = BuildContext(
            config=AppConfig(),
            mode="research",
            theme=Theme.from_mapping("research", {"typing": {}, "footer": {}, "quotes": []}),
            current_time_utc=datetime.now(timezone.utc),
            current_time_local=datetime.now(timezone.utc),
        )
        self.assertEqual(plugin.render(context), "")

    def test_configured_urls_render_sections(self):
        plugin = BuiltinProfileCardsPlugin()
        config = AppConfig(
            spotify_now_playing_url="https://example.com/spotify.svg",
            leetcode_card_url="https://example.com/leetcode.svg",
            blog_feed_url="https://example.com/blog",
            weather_card_url="https://example.com/weather.svg",
        )
        context = BuildContext(
            config=config,
            mode="research",
            theme=Theme.from_mapping("research", {"typing": {}, "footer": {}, "quotes": []}),
            current_time_utc=datetime.now(timezone.utc),
            current_time_local=datetime.now(timezone.utc),
        )
        output = plugin.render(context)
        self.assertIn("## Spotify", output)
        self.assertIn("## LeetCode", output)
        self.assertIn("## Latest Blog", output)
        self.assertIn("## Weather", output)


if __name__ == "__main__":
    unittest.main()
