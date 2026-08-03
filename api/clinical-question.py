"""Vercel-style wrapper for /api/clinical-question.

Deployments that use another platform can call
`serverless.clinical_question.handle_json_request` directly.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler

from serverless.clinical_question import MAX_REQUEST_BODY_BYTES, _cors_headers, handle_json_request


class handler(BaseHTTPRequestHandler):  # pylint: disable=invalid-name
    def _send_json(self, status: int, headers: dict[str, str], payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send_json(204, _cors_headers(), {})

    def do_POST(self) -> None:  # noqa: N802
        try:
            length = int(self.headers.get("Content-Length") or "0")
        except ValueError:
            self._send_json(400, _cors_headers(), {"status": "error", "message": "Invalid Content-Length"})
            return
        if length < 0 or length > MAX_REQUEST_BODY_BYTES:
            self._send_json(413, _cors_headers(), {"status": "error", "message": "Request body too large"})
            return
        try:
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        except UnicodeDecodeError:
            self._send_json(400, _cors_headers(), {"status": "error", "message": "Request body must be UTF-8 JSON"})
            return
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self._send_json(400, _cors_headers(), {"status": "error", "message": "Invalid JSON body"})
            return
        if not isinstance(payload, dict):
            self._send_json(400, _cors_headers(), {"status": "error", "message": "JSON request body must be an object"})
            return
        status, headers, response = handle_json_request(
            payload,
            request_meta={
                "headers": dict(self.headers.items()),
                "client_ip": self.client_address[0] if self.client_address else "",
            },
        )
        self._send_json(status, headers, response)

