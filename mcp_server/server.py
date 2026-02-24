from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

mcp = FastMCP("Demo server!")

@mcp.tool
def add(a: int, b: int) -> int:
    return a + b

@mcp.custom_route(
    "/health",
    methods=["GET"],
    include_in_schema=False
)
async def health(_: Request):
    return JSONResponse({"status": "ok"})


def run():
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    run()