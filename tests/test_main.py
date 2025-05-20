import http.client
import threading

import mcp_fabric
from mcp_fabric.main import RestHandler, HTTPServer


def test_server_registered():
    assert "mcp-fabric-rest" in mcp_fabric.SERVERS
