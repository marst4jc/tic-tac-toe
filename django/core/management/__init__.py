"""Slimmed-down management command runner."""

from __future__ import annotations

import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterable, List, Tuple

from django.conf import settings
from django.http import HttpResponse
from django.urls import URLPattern, URLResolver


class Request:
    """Very small request placeholder."""

    def __init__(self, path: str) -> None:
        self.path = path


def _flatten_urlpatterns(patterns: Iterable[URLPattern | URLResolver], prefix: str = "") -> List[Tuple[str, callable]]:
    flat: List[Tuple[str, callable]] = []
    for pattern in patterns:
        if isinstance(pattern, URLResolver):
            flat.extend(_flatten_urlpatterns(pattern.patterns, prefix + pattern.prefix))
        elif isinstance(pattern, URLPattern):
            flat.append((prefix + pattern.pattern, pattern.view))
    return flat


def _load_urlpatterns() -> List[Tuple[str, callable]]:
    """Load urlpatterns from the configured root URLConf."""

    if not hasattr(settings, "ROOT_URLCONF"):
        return []
    module = __import__(settings.ROOT_URLCONF, fromlist=["urlpatterns"])
    patterns = getattr(module, "urlpatterns", [])
    return _flatten_urlpatterns(patterns)


def _serve_static_file(base_dir: Path, static_url: str, request_path: str) -> bytes | None:
    if not request_path.startswith(static_url):
        return None
    stripped = request_path[len(static_url) :].lstrip("/")
    static_dirs = getattr(settings, "STATICFILES_DIRS", [])
    candidate_dirs = [Path(p) for p in static_dirs] or [base_dir / "static"]
    for directory in candidate_dirs:
        candidate = directory / stripped
        if candidate.exists() and candidate.is_file():
            return candidate.read_bytes()
    return None


def _run_simple_server(host: str, port: int) -> None:
    urlpatterns = _load_urlpatterns()
    base_dir = getattr(settings, "BASE_DIR", Path.cwd())
    static_url = getattr(settings, "STATIC_URL", "/static/")
    static_url = static_url if static_url.startswith("/") else f"/{static_url}"
    static_url = static_url if static_url.endswith("/") else f"{static_url}/"

    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            # Serve static assets first
            static_content = _serve_static_file(base_dir, static_url, self.path)
            if static_content is not None:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(static_content)
                return

            # Match URL patterns
            lookup_path = self.path.lstrip("/")
            for pattern, view in urlpatterns:
                normalized = pattern.lstrip("/")
                if normalized.endswith("/") and lookup_path == normalized[:-1]:
                    normalized = normalized[:-1]
                if lookup_path in {normalized, f"{normalized}/"} or (
                    not normalized and self.path in {"/", ""}
                ):
                    response = view(Request(self.path))
                    if not isinstance(response, HttpResponse):
                        response = HttpResponse(str(response))
                    self.send_response(response.status_code)
                    for header, value in response.headers.items():
                        self.send_header(header, value)
                    self.end_headers()
                    self.wfile.write(response.content)
                    return

            self.send_error(404, "Not Found")

        def log_message(self, format: str, *args: object) -> None:  # noqa: A003
            # Reduce noisy logs; mirror Django's concise output.
            sys.stderr.write("%s - - %s\n" % (self.address_string(), format % args))

    httpd = ThreadingHTTPServer((host, port), Handler)
    sys.stdout.write(f"Starting lightweight server at http://{host}:{port}\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:  # pragma: no cover - manual exit
        sys.stdout.write("Server stopped by user.\n")
    finally:
        httpd.server_close()


def _parse_address(value: str | None) -> tuple[str, int]:
    default_host, default_port = "127.0.0.1", 8000
    if not value:
        return default_host, default_port
    if ":" in value:
        host, port = value.split(":", 1)
        return host or default_host, int(port)
    return default_host, int(value)


def execute_from_command_line(argv: list[str] | None = None) -> None:
    """Entry point compatible with Django's manage.py.

    Only the ``runserver`` command is supported by this stub. Other commands
    prompt the user to install real Django.
    """

    argv = argv or sys.argv
    if len(argv) < 2:
        sys.stdout.write("Usage: manage.py runserver [addr:port]\n")
        return

    command = argv[1]
    if command != "runserver":
        sys.stderr.write(
            f"Command '{command}' is not available in the lightweight stub. "
            "Install Django for full management commands.\n"
        )
        sys.exit(1)

    host, port = _parse_address(argv[2] if len(argv) > 2 else None)
    _run_simple_server(host, port)
