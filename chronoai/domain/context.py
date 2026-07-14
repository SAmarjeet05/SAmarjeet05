from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from chronoai.config.app import AppConfig
from chronoai.domain.theme import Theme


@dataclass(frozen=True)
class BuildContext:
    config: AppConfig
    mode: str
    theme: Theme
    current_time_utc: datetime
    current_time_local: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    def with_metadata(self, **metadata: Any) -> "BuildContext":
        merged = dict(self.metadata)
        merged.update(metadata)
        return BuildContext(
            config=self.config,
            mode=self.mode,
            theme=self.theme,
            current_time_utc=self.current_time_utc,
            current_time_local=self.current_time_local,
            metadata=merged,
        )