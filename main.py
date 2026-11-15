from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("CustomWeatherAndMathServer")

@mcp.tool()
def calculate_compound_interest(principal: float, rate: float, years: int) -> str:
    """Calculates compound interest given principal, annual rate (as decimal), and years."""
    amount = principal * ((1 + rate) ** years)
    return f"Total amount after {years} years: ${amount:.2f}"

@mcp.tool()
def get_server_status(service_name: str) -> str:
    """Checks the operational status of an internal service."""
    statuses = {"auth": "Operational", "billing": "Degraded", "database": "Operational"}
    status = statuses.get(service_name.lower(), "Unknown service")
    return f"Service '{service_name}' status: {status}"

if __name__ == "__main__":
    # Runs the server over standard input/output (stdio)
    mcp.run(transport="stdio")
