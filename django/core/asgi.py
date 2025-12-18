"""Placeholder ASGI application factory."""

from __future__ import annotations

from typing import Any


def get_asgi_application() -> Any:  # pragma: no cover - compatibility only
    """Return a no-op ASGI application."""

    async def application(scope: dict[str, Any], receive: Any, send: Any) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": 501,
                "headers": [(b"content-type", b"text/plain")],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": b"ASGI support is unavailable in the lightweight stub.",
            }
        )

    return application
