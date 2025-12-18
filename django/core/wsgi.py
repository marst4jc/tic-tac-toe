"""Placeholder WSGI application factory."""

from __future__ import annotations

from typing import Any


def get_wsgi_application() -> Any:  # pragma: no cover - compatibility only
    """Return a no-op WSGI application."""

    def application(environ: dict[str, Any], start_response: Any) -> list[bytes]:
        start_response("501 Not Implemented", [("Content-Type", "text/plain")])
        return [b"WSGI support is unavailable in the lightweight stub."]

    return application
