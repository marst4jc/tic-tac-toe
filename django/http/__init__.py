"""Small HTTP helpers inspired by Django's interfaces."""

from __future__ import annotations

from typing import Any, Iterable


class HttpResponse:
    """Lightweight HTTP response container."""

    def __init__(
        self,
        content: str | bytes = "",
        *,
        status: int = 200,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.content = content.encode() if isinstance(content, str) else content
        self.status_code = status
        self.headers = headers or {}

    def __iter__(self) -> Iterable[bytes]:  # pragma: no cover - compatibility only
        yield self.content

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<HttpResponse status={self.status_code} bytes={len(self.content)}>"
