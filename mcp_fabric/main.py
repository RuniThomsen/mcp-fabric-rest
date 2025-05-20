"""Basic entry point for the MCP Fabric REST server."""

from __future__ import annotations

import argparse
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

# In-memory storage for created objects
WORKSPACES: list[dict[str, Any]] = []
"""Workspace records stored during runtime."""
ARTIFACTS: list[dict[str, Any]] = []
"""Artifact records stored during runtime."""


def run_server(server: HTTPServer) -> None:
    """Run the given server until interrupted."""

    print("mcp-fabric-rest server started", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


class RestHandler(BaseHTTPRequestHandler):
    """Simple REST request handler."""

    def _send_json(self, code: int, body: object) -> None:
        """Serialize ``body`` to JSON and send it with the given status code."""
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode("utf-8"))

    def log_message(self, format: str, *args: str) -> None:  # noqa: D401
        """Silence default logging."""
        return

    def do_GET(self) -> None:  # noqa: D401
        """Handle GET requests."""
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
        elif self.path == "/v1/workspaces":
            self._send_json(200, {"workspaces": WORKSPACES})
        elif self.path == "/v1/artifacts":
            self._send_json(200, {"artifacts": ARTIFACTS})
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: D401
        """Handle POST requests."""
        if self.path in {"/v1/workspaces", "/v1/artifacts"}:
            content_length = int(self.headers.get("Content-Length", 0))
            payload: Any = {}
            if content_length:
                body = self.rfile.read(content_length)
                try:
                    payload = json.loads(body.decode("utf-8"))
                except json.JSONDecodeError:
                    self.send_error(400, "Invalid JSON")
                    return

            if self.path == "/v1/workspaces":
                WORKSPACES.append(payload)
            else:
                ARTIFACTS.append(payload)

            self._send_json(201, {"created": True})
        else:
            self._send_json(404, {"error": "not found"})


def create_server(host: str = "localhost", port: int = 3000) -> HTTPServer:
    """Create the REST server instance.

    Parameters
    ----------
    host:
        Interface the HTTP server should bind to.
    port:
        Port the HTTP server should listen on.
    """

    return HTTPServer((host, port), RestHandler)


def run_rest_server(host: str = "localhost", port: int = 3000) -> None:
    """Start a REST HTTP server.

    Parameters
    ----------
    host:
        Interface the HTTP server should bind to.
    port:
        Port the HTTP server should listen on.
    """
    server = create_server(host, port)
    print(f"REST server listening on http://{host}:{port}", flush=True)
    try:
        run_server(server)
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="MCP Fabric REST server")
    parser.add_argument("--stdio", action="store_true", help="run server using stdio")
    parser.add_argument("--rest", action="store_true", help="run REST HTTP server")
    parser.add_argument(
        "--port", type=int, default=3000, help="port for REST HTTP server"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="host interface for REST HTTP server",
    )
    args = parser.parse_args(argv)

    threads: list[threading.Thread] = []

    if args.rest:
        thread = threading.Thread(
            target=run_rest_server,
            kwargs={"port": args.port, "host": args.host},
            daemon=args.stdio,
        )
        thread.start()
        threads.append(thread)

    if args.stdio:
        print("mcp-fabric-rest server started", flush=True)
        try:
            for line in sys.stdin:
                # Echo received lines back to stdout
                print(line.rstrip(), flush=True)
        except KeyboardInterrupt:
            pass

    if args.rest and not args.stdio:
        # Wait for the REST server thread when running alone
        threads[0].join()

    if not args.rest and not args.stdio:
        parser.print_help()


if __name__ == "__main__":
    main()
