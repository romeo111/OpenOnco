"""Local dev server for the optional clinical-question page.

It serves ``docs/`` and handles ``/api/clinical-question`` in one origin, so
the browser can call the endpoint without exposing ``OPENAI_API_KEY``.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from serverless.clinical_question import _cors_headers, handle_json_request


DOCS_ROOT = REPO_ROOT / "docs"
DEFAULT_PORT = 8787


def load_dotenv(path: Path) -> None:
    """Load simple KEY=VALUE lines without overriding real environment vars."""

    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


class LocalOpenOncoHandler(BaseHTTPRequestHandler):
    server_version = "OpenOncoAskLocal/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"{self.address_string()} - {fmt % args}")

    def _send_json(self, status: int, headers: dict[str, str], payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        if self.path == "/api/clinical-question":
            self._send_json(200, _cors_headers(), {"status": "ok"})
            return
        self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/clinical-question":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length") or "0")
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self._send_json(400, _cors_headers(), {"status": "error", "message": "Invalid JSON body"})
            return
        status, headers, response = handle_json_request(payload)
        self._send_json(status, headers, response)

    def do_GET(self) -> None:  # noqa: N802
        path = unquote(self.path.split("?", 1)[0])
        if path in ("", "/"):
            path = "/ukr/ask.html"
        target = (DOCS_ROOT / path.lstrip("/")).resolve()
        if not str(target).startswith(str(DOCS_ROOT.resolve())):
            self.send_error(403)
            return
        if target.is_dir():
            target = target / "index.html"
        if not target.exists() or not target.is_file():
            self.send_error(404)
            return
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve docs/ask.html with the local clinical-question API.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--env-file", default=str(REPO_ROOT / ".env"))
    args = parser.parse_args()

    load_dotenv(Path(args.env_file))
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not configured. Add it to .env or the environment before asking a case.")

    server = ThreadingHTTPServer((args.host, args.port), LocalOpenOncoHandler)
    print(f"Open http://{args.host}:{args.port}/ukr/ask.html")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
