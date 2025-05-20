"""Basic entry point for the MCP Fabric REST server."""

from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any


class RESTRequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler for the MCP Fabric REST API."""

    server_version = "mcp-fabric-rest"

    def _json_response(self, status: int, data: Any) -> None:
        """Send a JSON response."""

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self) -> None:  # noqa: D401
        """Handle GET requests."""

        if self.path == "/health":
            self._json_response(200, {"status": "ok"})
        elif self.path == "/v1/workspaces":
            self._json_response(200, {"workspaces": []})
        elif self.path == "/v1/artifacts":
            self._json_response(200, {"artifacts": []})
        else:
            self.send_error(404)

    def do_POST(self) -> None:  # noqa: D401
        """Handle POST requests."""

        if self.path in {"/v1/workspaces", "/v1/artifacts"}:
            # Consume the request body even though we don't use it
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length:
                self.rfile.read(content_length)
            self._json_response(201, {"created": True})
        else:
            self.send_error(404)


def create_server(host: str = "localhost", port: int = 3000) -> HTTPServer:
    """Create the REST server instance."""

    return HTTPServer((host, port), RESTRequestHandler)


def run_server() -> None:
    """Run the MCP Fabric REST server."""

    server = create_server()
    print("mcp-fabric-rest server started", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="MCP Fabric REST server")
    parser.add_argument("--stdio", action="store_true", help="run server using stdio")
    args = parser.parse_args(argv)

    if args.stdio:
        run_server()
        try:
            for line in sys.stdin:
                # Echo received lines back to stdout
                print(line.rstrip(), flush=True)
        except KeyboardInterrupt:
            pass
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
