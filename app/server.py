"""Dependency-free local demo server; not intended as an internet-facing production server."""
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .agent import build_plan, plan_to_dict
from .audit import AuditLog

ROOT = Path(__file__).resolve().parent.parent
AUDIT = AuditLog()
MAX_BODY_BYTES = 16_384
MAX_MESSAGE_CHARS = 4_000


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "web"), **kwargs)

    def _json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/health":
            return self._json(
                200, {"status": "ok", "service": "Dubai Nexus AI", "mode": "safe-demo"}
            )
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/agent/plan":
            return self._json(404, {"error": "Not found"})

        try:
            raw_length = self.headers.get("Content-Length", "0")
            length = int(raw_length)
            if length <= 0 or length > MAX_BODY_BYTES:
                return self._json(
                    413, {"error": "Request body must be between 1 and 16384 bytes."}
                )

            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                return self._json(400, {"error": "JSON body must be an object."})

            message = payload.get("message", "")
            if not isinstance(message, str) or len(message) > MAX_MESSAGE_CHARS:
                return self._json(
                    400, {"error": "message must be a string of at most 4000 characters."}
                )

            plan = plan_to_dict(build_plan(message))
            AUDIT.append(
                "plan_created",
                {
                    "plan_id": plan["plan_id"],
                    "intent": plan["intent"],
                    "language": plan["language"],
                },
            )
            return self._json(200, {"plan": plan})
        except (ValueError, json.JSONDecodeError) as exc:
            return self._json(400, {"error": str(exc)})


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8080), Handler)
    print("Dubai Nexus AI running at http://127.0.0.1:8080")
    server.serve_forever()


if __name__ == "__main__":
    main()
