import pytest
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.utilities.tests import run_server_async

from store_sim_mcp.server import mcp


@pytest.fixture
async def http_server() -> str:
    """Start server in-process for testing."""
    async with run_server_async(mcp) as url:
        yield url

@pytest.mark.asyncio
async def test_http_transport(http_server: str):
    """Test actual HTTP transport behavior."""
    async with Client(
        transport=StreamableHttpTransport(http_server)
    ) as client:
        result = await client.ping()
        assert result is True

        tools = await client.list_tools()
        EXPECTED_TOOLS = [
            "get_customer_info",
            "get_order_info",
            "check_inventory",
            "get_customer_ids_by_name",
            "get_orders_by_customer_id"
        ]
        assert set(EXPECTED_TOOLS) == set(t.name for t in tools)
