"""Basic entry point for the MCP Fabric REST server."""

from __future__ import annotations

import argparse
import sys


def run_server() -> None:
    """Placeholder server implementation."""
    print("mcp-fabric-rest server started", flush=True)


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
