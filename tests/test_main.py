import http.client
import threading

import mcp_fabric
from mcp_fabric.main import RestHandler, HTTPServer


def test_server_registered():
    assert "mcp-fabric-rest" in mcp_fabric.SERVERS


def _start_server():
    server = HTTPServer(("localhost", 0), RestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def test_health_endpoint():
    server, thread = _start_server()
    port = server.server_address[1]
    conn = http.client.HTTPConnection("localhost", port)
    conn.request("GET", "/health")
    response = conn.getresponse()
    body = response.read().decode()
    conn.close()
    server.shutdown()
    thread.join()
    assert response.status == 200
    assert body == '{"status": "ok"}'


def test_workspaces_and_artifacts():
    server, thread = _start_server()
    port = server.server_address[1]
    conn = http.client.HTTPConnection("localhost", port)

    conn.request("GET", "/v1/workspaces")
    resp = conn.getresponse()
    body = resp.read().decode()
    assert resp.status == 200
    assert body == "[]"

    conn.request("POST", "/v1/artifacts")
    resp = conn.getresponse()
    body = resp.read().decode()
    assert resp.status == 201
    assert body == "{}"

    conn.close()
    server.shutdown()
    thread.join()
