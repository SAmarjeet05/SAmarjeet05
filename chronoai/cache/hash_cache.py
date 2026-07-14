from __future__ import annotations

import hashlib
import os


class HashCache:
    @staticmethod
    def compute(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def read(path: str) -> str | None:
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as file_handle:
            value = file_handle.read().strip()
        return value or None

    @staticmethod
    def write(path: str, digest: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file_handle:
            file_handle.write(digest)