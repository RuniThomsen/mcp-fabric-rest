import pytest
from mcp_fabric_rest import register


@pytest.mark.compliance
def test_register():
    """Ensure the placeholder register call succeeds."""
    assert register() is True
