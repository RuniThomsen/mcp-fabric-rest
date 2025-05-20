import mcp_fabric


def test_server_registered():
    assert "mcp-fabric-rest" in mcp_fabric.SERVERS
