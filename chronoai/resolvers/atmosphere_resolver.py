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
        minutes = now.hour * 60 + now.minute

        # Boundaries in minutes since midnight:
        # - 06:00 IST = 360 mins
        # - 11:00 IST = 660 mins
        # - 17:30 IST = 1050 mins
        # - 21:30 IST = 1290 mins
        if 360 <= minutes < 660:
            return "boot"
        if 660 <= minutes < 1050:
            return "inference"
        if 1050 <= minutes < 1290:
            return "optimization"
        return "research"