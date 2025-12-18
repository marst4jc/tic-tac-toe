"""Tiny URL dispatcher inspired by Django."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any, Callable, Iterable, List

View = Callable[..., Any]


@dataclass
class URLPattern:
    pattern: str
    view: View
    name: str | None = None


@dataclass
class URLResolver:
    prefix: str
    patterns: List[URLPattern]


def path(route: str, view: View | URLResolver, name: str | None = None) -> URLPattern | URLResolver:
    """Return a URL pattern or resolver.

    - If *view* is a callable, produce a URLPattern.
    - If *view* is a URLResolver, produce a new resolver with the provided prefix.
    """

    if isinstance(view, URLResolver):
        return URLResolver(route, view.patterns)
    return URLPattern(route, view, name)


def include(arg: str | Iterable[URLPattern]) -> URLResolver:
    """Return URL patterns from a module or iterable."""

    if isinstance(arg, str):
        module = importlib.import_module(arg)
        patterns = getattr(module, "urlpatterns", [])
    else:
        patterns = list(arg)
    return URLResolver("", patterns)
