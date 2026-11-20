
import platform
import sys
import socket
import shutil
from pathlib import Path
from datetime import datetime

import psutil
from fastmcp import FastMCP
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# Initialize MCP server
mcp = FastMCP("SystemUtilityServer")


# --------------------------------------------------
# TOOL 1: Compound Interest Calculator
# --------------------------------------------------

@mcp.tool()
def calculate_compound_interest(
    principal: float,
    rate: float,
    years: int
) -> dict:
    """Calculate compound interest using principal, annual rate, and years.

    Rate must be provided as a decimal. For example, 5% = 0.05.
    """

    if principal < 0:
        return {"error": "Principal cannot be negative."}

    if rate < 0:
        return {"error": "Interest rate cannot be negative."}

    if years < 0:
        return {"error": "Years cannot be negative."}

    amount = principal * ((1 + rate) ** years)
    interest = amount - principal

    return {
        "principal": principal,
        "annual_rate": rate,
        "years": years,
        "total_amount": round(amount, 2),
        "interest_earned": round(interest, 2)
    }


# --------------------------------------------------
# TOOL 2: Service Status
# --------------------------------------------------

@mcp.tool()
def get_server_status(service_name: str) -> dict:
    """Check the operational status of a predefined service."""

    statuses = {
        "auth": "Operational",
        "billing": "Degraded",
        "database": "Operational"
    }

    status = statuses.get(service_name.lower())

    if status is None:
        return {
            "service": service_name,
            "status": "Unknown",
            "message": "Service is not registered."
        }

    return {
        "service": service_name,
        "status": status
    }


# --------------------------------------------------
# TOOL 3: System Information
# --------------------------------------------------

@mcp.tool()
def get_system_info() -> dict:
    """Get operating system, CPU, RAM, and Python information."""

    memory = psutil.virtual_memory()

    return {
        "operating_system": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "cpu_logical_cores": psutil.cpu_count(logical=True),
        "cpu_physical_cores": psutil.cpu_count(logical=False),
        "total_ram_gb": round(memory.total / (1024 ** 3), 2),
        "available_ram_gb": round(memory.available / (1024 ** 3), 2),
        "ram_usage_percent": memory.percent,
        "python_version": sys.version.split()[0],
        "hostname": socket.gethostname()
    }


# --------------------------------------------------
# TOOL 4: Disk Usage
# --------------------------------------------------

@mcp.tool()
def get_disk_usage(path: str = ".") -> dict:
    """Get total, used, and free disk space for a given path."""

    try:
        disk = shutil.disk_usage(path)

        return {
            "path": str(Path(path).resolve()),
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
            "usage_percent": round(
                (disk.used / disk.total) * 100, 2
            )
        }

    except (OSError, ValueError) as e:
        return {
            "error": str(e)
        }


# --------------------------------------------------
# TOOL 5: Website Availability
# --------------------------------------------------

@mcp.tool()
def check_website_status(url: str) -> dict:
    """Check whether a website responds to an HTTP request."""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        request = Request(
            url,
            headers={"User-Agent": "MCP-Monitor/1.0"},
            method="GET"
        )

        with urlopen(request, timeout=10) as response:

            return {
                "url": url,
                "status_code": response.status,
                "available": True,
                "message": "Website responded successfully."
            }

    except HTTPError as e:

        # HTTP errors still mean the website responded.
        return {
            "url": url,
            "status_code": e.code,
            "available": True,
            "message": f"Website responded with HTTP {e.code}."
        }

    except (URLError, TimeoutError, OSError) as e:

        return {
            "url": url,
            "available": False,
            "message": str(e)
        }


# --------------------------------------------------
# TOOL 6: Network Information
# --------------------------------------------------

@mcp.tool()
def get_network_info() -> dict:
    """Get hostname and the local IP address of this machine."""

    hostname = socket.gethostname()

    try:

        # Determine local IP used for outbound connections
        connection = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        connection.connect(("8.8.8.8", 80))

        local_ip = connection.getsockname()[0]

        connection.close()

    except OSError:

        local_ip = "Unavailable"

    return {
        "hostname": hostname,
        "local_ip_address": local_ip
    }


# --------------------------------------------------
# TOOL 7: Current Date and Time
# --------------------------------------------------

@mcp.tool()
def get_current_datetime() -> dict:
    """Get the current local date, time, and timezone."""

    now = datetime.now().astimezone()

    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timezone": str(now.tzinfo),
        "iso_format": now.isoformat()
    }


# --------------------------------------------------
# TOOL 8: List Files
# --------------------------------------------------

@mcp.tool()
def list_files(directory: str = ".") -> dict:
    """List all files and folders in a directory.

    If the user does not specify a directory, automatically list
    the contents of the current working directory ('.').
    """

    try:

        path = Path(directory).expanduser().resolve()

        if not path.exists():
            return {"error": "Directory does not exist."}

        if not path.is_dir():
            return {"error": "The provided path is not a directory."}

        items = []

        for item in path.iterdir():

            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file"
            })

        return {
            "directory": str(path),
            "total_items": len(items),
            "items": items
        }

    except PermissionError:
        return {
            "error": "Permission denied."
        }

    except OSError as e:
        return {
            "error": str(e)
        }


# --------------------------------------------------
# Run MCP Server
# --------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
