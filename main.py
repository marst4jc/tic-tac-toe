from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os


DEFAULT_PORT = 8000
STATIC_DIR = Path(__file__).parent / "web"


class TicTacToeRequestHandler(SimpleHTTPRequestHandler):
    """Serve static files with a fallback favicon handler."""

    def do_GET(self):
        self._reroute_favicon()
        return super().do_GET()

    def do_HEAD(self):
        self._reroute_favicon()
        return super().do_HEAD()

    def _reroute_favicon(self):
        if self.path == "/favicon.ico":
            self.path = "/favicon.svg"


def run_server(port: int = DEFAULT_PORT) -> None:
    """Serve the React front-end from the local web directory."""

    if not STATIC_DIR.exists():
        raise FileNotFoundError(f"Static directory not found: {STATIC_DIR}")

    handler = partial(TicTacToeRequestHandler, directory=str(STATIC_DIR))
    with ThreadingHTTPServer(("0.0.0.0", port), handler) as httpd:
        print("\nTic-Tac-Toe React UI running!")
        print(f"Visit http://localhost:{port} to play. Press Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


def main():
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    run_server(port)


if __name__ == "__main__":
    main()
