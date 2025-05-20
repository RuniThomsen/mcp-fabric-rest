import json
import socket
import threading
import time
from urllib import request

import pytest

from mcp_fabric.main import create_server


@pytest.fixture(scope="module")
def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("localhost", 0))
        port = sock.getsockname()[1]

    srv = create_server(port=port)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.1)
    try:
        yield srv
    finally:
        srv.shutdown()
        thread.join()


def _request(server, path: str, data: bytes | None = None, method: str = "GET"):
    req = request.Request(
        f"http://localhost:{server.server_port}{path}", data=data, method=method
    )
    req.add_header("Content-Type", "application/json")
    with request.urlopen(req) as resp:
        body = resp.read()
        return resp.status, json.loads(body)


def test_health(server):
    status, body = _request(server, "/health")
    assert status == 200
    assert body == {"status": "ok"}


def test_workspaces_get(server):
    status, body = _request(server, "/v1/workspaces")
    assert status == 200
    assert body == {"workspaces": []}


def test_workspaces_post(server):
    data = json.dumps({"name": "test"}).encode()
    status, body = _request(server, "/v1/workspaces", data=data, method="POST")
    assert status == 201
    assert body == {"created": True}


def test_artifacts_get(server):
    status, body = _request(server, "/v1/artifacts")
    assert status == 200
    assert body == {"artifacts": []}


def test_artifacts_post(server):
    data = json.dumps({"name": "test"}).encode()
    status, body = _request(server, "/v1/artifacts", data=data, method="POST")
    assert status == 201
    assert body == {"created": True}
