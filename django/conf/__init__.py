"""Minimal settings loader to mimic Django's settings access pattern."""

from __future__ import annotations

import importlib
import os
from types import SimpleNamespace
from typing import Any


class LazySettings:
    """Tiny stand-in for Django's lazy settings wrapper."""

    def __init__(self) -> None:
        self._wrapped: Any | None = None

    def _setup(self) -> None:
        settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")
        if not settings_module:
            raise RuntimeError(
                "DJANGO_SETTINGS_MODULE is not set. "
                "Set it to your settings module (e.g. 'tictactoe.settings')."
            )
        self._wrapped = importlib.import_module(settings_module)

    def __getattr__(self, name: str) -> Any:  # pragma: no cover - trivial passthrough
        if self._wrapped is None:
            self._setup()
        return getattr(self._wrapped, name)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        if self._wrapped is None:
            return "<LazySettings [Unevaluated]>"
        return repr(self._wrapped)


settings = LazySettings()


def global_settings() -> SimpleNamespace:
    """Return a minimal default settings object."""

    return SimpleNamespace(DEBUG=False)
