"""Lightweight, built-in Django stub used for offline execution.

This project is designed to run without installing the real Django package,
which is unavailable in the execution environment. The stub provides just
enough surface area for the Tic-Tac-Toe app to serve its single page and
static assets. For full Django functionality, install Django in an
environment with internet access.
"""

__all__ = ["get_version"]
__version__ = "0.0.0-localstub"


def get_version() -> str:
    """Return the local stub version string."""

    return __version__
