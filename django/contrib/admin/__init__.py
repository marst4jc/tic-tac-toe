"""Stub admin site so url imports continue to work."""

from __future__ import annotations

from django.http import HttpResponse
from django.urls import URLPattern, path


def _admin_placeholder_view(request: object) -> HttpResponse:
    return HttpResponse(
        "Admin interface is unavailable in the lightweight stub.", status=501
    )


class AdminSite:
    @property
    def urls(self) -> list[URLPattern]:
        return [path("", _admin_placeholder_view, name="admin:index")]


site = AdminSite()
