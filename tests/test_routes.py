import json
import threading
import time
from urllib import request

import pytest

from mcp_fabric.main import create_server


@pytest.fixture(scope="module")
def server():
    srv = create_server()
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.1)
    try:
        yield srv
    finally:
        srv.shutdown()
        thread.join()


def _request(path: str, data: bytes | None = None, method: str = "GET"):
    req = request.Request(f"http://localhost:3000{path}", data=data, method=method)
    req.add_header("Content-Type", "application/json")
    with request.urlopen(req) as resp:
        body = resp.read()
        return resp.status, json.loads(body)


def test_health(server):
    status, body = _request("/health")
    assert status == 200
    assert body == {"status": "ok"}


def test_workspaces_get(server):
    status, body = _request("/v1/workspaces")
    assert status == 200
    assert body == {"workspaces": []}


def test_workspaces_post(server):
    data = json.dumps({"name": "test"}).encode()
    status, body = _request("/v1/workspaces", data=data, method="POST")
    assert status == 201
    assert body == {"created": True}


def test_artifacts_get(server):
    status, body = _request("/v1/artifacts")
    assert status == 200
    assert body == {"artifacts": []}


def test_artifacts_post(server):
    data = json.dumps({"name": "test"}).encode()
    status, body = _request("/v1/artifacts", data=data, method="POST")
    assert status == 201
    assert body == {"created": True}
