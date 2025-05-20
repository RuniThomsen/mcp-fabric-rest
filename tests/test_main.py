import json
import socket
import subprocess
import sys
import time
from urllib import request

import mcp_fabric


def test_server_registered():
    assert "mcp-fabric-rest" in mcp_fabric.SERVERS


def test_cli_rest_server_health():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("localhost", 0))
        port = sock.getsockname()[1]

    proc = subprocess.Popen(
        [sys.executable, "-m", "mcp_fabric.main", "--rest", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        for _ in range(20):
            try:
                with request.urlopen(f"http://localhost:{port}/health") as resp:
                    body = resp.read()
                    assert resp.status == 200
                    assert json.loads(body) == {"status": "ok"}
                    break
            except Exception:
                if proc.poll() is not None:
                    out, err = proc.communicate()
                    raise AssertionError(f"server exited\nstdout: {out}\nstderr: {err}")
                time.sleep(0.1)
        else:
            raise AssertionError("server did not start")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
