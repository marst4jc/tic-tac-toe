"""Minimal shortcuts module with template rendering support."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from django.conf import settings
from django.http import HttpResponse


STATIC_PATTERN = re.compile(r"{%\\s*static\\s+['\\\"]([^'\\\"]+)['\\\"]\\s*%}")


def _locate_template(template_name: str) -> Path:
    base_dir = getattr(settings, "BASE_DIR", Path.cwd())
    # Search template directories declared in settings
    for template in getattr(settings, "TEMPLATES", []):
        for directory in template.get("DIRS", []):
            candidate = Path(directory) / template_name
            if candidate.exists():
                return candidate
    # Fallback: search under the project tree
    for candidate in base_dir.rglob(template_name):
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Template '{template_name}' not found.")


def render(request: Any, template_name: str, context: dict[str, Any] | None = None, *args: Any, **kwargs: Any) -> HttpResponse:
    """Render a template by performing a tiny subset of Django's behavior."""

    template_path = _locate_template(template_name)
    content = template_path.read_text(encoding="utf-8")
    # Remove `{% load static %}` declarations and replace static tags.
    content = content.replace("{% load static %}", "")
    content = STATIC_PATTERN.sub(r"/static/\\1", content)
    return HttpResponse(content)
