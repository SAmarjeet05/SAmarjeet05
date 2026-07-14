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
