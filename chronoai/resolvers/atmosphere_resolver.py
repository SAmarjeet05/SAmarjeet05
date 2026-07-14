from __future__ import annotations

from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None


class AtmosphereResolver:
    @staticmethod
    def local_now(timezone_name: str = "Asia/Kolkata") -> datetime:
        if ZoneInfo is not None:
            try:
                return datetime.now(timezone.utc).astimezone(ZoneInfo(timezone_name))
            except Exception:
                pass

        return datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)

    @staticmethod
    def resolve_mode(now: datetime) -> str:
        hour = now.hour

        if 6 <= hour < 12:
            return "boot"
        if 12 <= hour < 18:
            return "inference"
        if 18 <= hour < 22:
            return "optimization"
        return "research"