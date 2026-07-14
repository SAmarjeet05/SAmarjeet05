from __future__ import annotations


class BuiltinProfileCardsPlugin:
    name = "builtin-profile-cards"

    def render(self, context) -> str:
        sections: list[str] = []

        spotify = self._render_spotify(context)
        if spotify:
            sections.append(spotify)

        leetcode = self._render_leetcode(context)
        if leetcode:
            sections.append(leetcode)

        blog = self._render_blog(context)
        if blog:
            sections.append(blog)

        weather = self._render_weather(context)
        if weather:
            sections.append(weather)

        return "\n\n".join(sections)

    def _render_spotify(self, context) -> str:
        url = context.config.spotify_now_playing_url.strip()
        if not url:
            return ""

        return (
            "## Spotify\n\n"
            "<p align=\"center\">\n"
            f"<img src=\"{url}\" alt=\"Spotify now playing\" width=\"60%\"/>\n"
            "</p>"
        )

    def _render_leetcode(self, context) -> str:
        url = context.config.leetcode_card_url.strip()
        if not url:
            return ""

        return (
            "## LeetCode\n\n"
            "<p align=\"center\">\n"
            f"<img src=\"{url}\" alt=\"LeetCode stats\" width=\"60%\"/>\n"
            "</p>"
        )

    def _render_blog(self, context) -> str:
        url = context.config.blog_feed_url.strip()
        if not url:
            return ""

        return (
            "## Latest Blog\n\n"
            "<p align=\"center\">\n"
            f"<a href=\"{url}\">Read recent posts</a>\n"
            "</p>"
        )

    def _render_weather(self, context) -> str:
        url = context.config.weather_card_url.strip()
        if not url:
            return ""

        return (
            "## Weather\n\n"
            "<p align=\"center\">\n"
            f"<img src=\"{url}\" alt=\"Weather card\" width=\"60%\"/>\n"
            "</p>"
        )