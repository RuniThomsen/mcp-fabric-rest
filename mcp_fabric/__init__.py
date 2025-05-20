"""mcp_fabric package initialization."""

from typing import Callable, Dict

# Simple registry for available server entrypoints.
SERVERS: Dict[str, Callable[[], None]] = {}


def register_server(name: str, handler: Callable[[], None]) -> None:
    """Register a server entry point.

    Parameters
    ----------
    name:
        The server name.
    handler:
        Callable that starts the server.
    """
    SERVERS[name] = handler


# Import main server and register it when package is imported
from .main import run_server
register_server("mcp-fabric-rest", run_server)
__all__ = ["register_server", "SERVERS", "run_server"]
