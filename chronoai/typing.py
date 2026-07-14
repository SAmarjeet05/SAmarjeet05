from __future__ import annotations

import random


class TypingManager:
    @staticmethod
    def get_lines_query(typing_config, shuffle=True):
        """Prepares a semicolon-separated, plus-encoded query string for Typing SVG."""
        lines = list(typing_config.get("lines", []))
        if not lines:
            return ""

        if shuffle:
            random.shuffle(lines)

        # Encode spaces to plus (+) for typing svg url compatibility
        encoded_lines = [line.replace(" ", "+") for line in lines]
        return ";".join(encoded_lines)

    @staticmethod
    def get_color(typing_config):
        return typing_config.get("color", "default")

    @staticmethod
    def build_typing_url(context, shuffle=True):
        typing_config = context.theme.get("typing", {})
        color = TypingManager.get_color(typing_config)
        lines = TypingManager.get_lines_query(typing_config, shuffle=shuffle)
        return (
            "https://readme-typing-svg.herokuapp.com?"
            "font=Fira+Code&weight=500&size=22&duration=3500&pause=1000&"
            f"color={color}&center=true&vCenter=true&width=750&lines={lines}"
        )
