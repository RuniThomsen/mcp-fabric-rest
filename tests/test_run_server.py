import json
import socket
import threading
import time
from urllib import request

import pytest

from mcp_fabric.main import (
    ARTIFACTS,
    WORKSPACES,
    create_server,
    run_server,
)


@pytest.fixture(scope="module")
def run_srv():
    WORKSPACES.clear()
    ARTIFACTS.clear()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("localhost", 0))
        port = sock.getsockname()[1]

    srv = create_server(port=port)
    thread = threading.Thread(target=run_server, args=(srv,), daemon=True)
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


def test_run_server_health(run_srv):
    status, body = _request(run_srv, "/health")
    assert status == 200
    assert body == {"status": "ok"}


def test_run_server_workspaces_get(run_srv):
    status, body = _request(run_srv, "/v1/workspaces")
    assert status == 200
    assert body == {"workspaces": []}


def test_run_server_workspaces_post(run_srv):
    data = json.dumps({"name": "test"}).encode()
    status, body = _request(run_srv, "/v1/workspaces", data=data, method="POST")
    assert status == 201
    assert body == {"created": True}

    status, body = _request(run_srv, "/v1/workspaces")
    assert status == 200
    assert body == {"workspaces": [{"name": "test"}]}


def test_run_server_artifacts_get(run_srv):
    status, body = _request(run_srv, "/v1/artifacts")
    assert status == 200
    assert body == {"artifacts": []}


def test_run_server_artifacts_post(run_srv):
    data = json.dumps({"name": "test"}).encode()
    status, body = _request(run_srv, "/v1/artifacts", data=data, method="POST")
    assert status == 201
    assert body == {"created": True}

    status, body = _request(run_srv, "/v1/artifacts")
    assert status == 200
    assert body == {"artifacts": [{"name": "test"}]}
