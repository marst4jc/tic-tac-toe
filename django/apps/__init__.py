"""Placeholder AppConfig to keep Django-style apps importable."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class AppConfig:
    name: str
    label: str | None = None

    def __init__(self, name: str, app_name: str | None = None) -> None:
        self.name = name
        self.label = app_name or name.rsplit(".", 1)[-1]

    def ready(self) -> None:  # pragma: no cover - noop hook
        """Compatibility hook for subclasses."""
        return None
