"""
👋 Welcome to your Smithery project!
To run your server, use "uv run dev"
To test interactively, use "uv run playground"

You might find this resources useful:

🧑‍💻 MCP's Python SDK (helps you define your server)
https://github.com/modelcontextprotocol/python-sdk
"""

from typing import Any
import httpx
from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

from smithery.decorators import smithery

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Optional: If you want to receive session-level config from user, define it here
class ConfigSchema(BaseModel):
    # access_token: str = Field(..., description="Your access token for authentication")
    pirate_mode: bool = Field(False, description="Speak like a pirate")

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

# For servers with configuration:
@smithery.server(config_schema=ConfigSchema)
# For servers without configuration, simply use:
# @smithery.server()
def create_server():
    """Create and configure the MCP server."""

    # Create your FastMCP server as usual
    server = FastMCP("Say Hello")

    # Add a tool
    @server.tool()
    def hello(name: str, ctx: Context) -> str:
        """Say hello to someone."""
        # Access session-specific config through context
        session_config = ctx.session_config

        # In real apps, use token for API requests:
        # requests.get(url, headers={"Authorization": f"Bearer {session_config.access_token}"})
        # if not session_config.access_token:
        #     return "Error: Access token required"

        # Create greeting based on pirate mode
        if session_config.pirate_mode:
            return f"Ahoy, {name}!"
        else:
            return f"Hello, {name}!"

    # Add a resource
    @server.resource("history://hello-world")
    def hello_world() -> str:
        """The origin story of the famous 'Hello, World' program."""
        return (
            '"Hello, World" first appeared in a 1972 Bell Labs memo by '
            "Brian Kernighan and later became the iconic first program "
            "for beginners in countless languages."
        )

    # Add a prompt
    @server.prompt()
    def greet(name: str) -> list:
        """Generate a greeting prompt."""
        return [
            {
                "role": "user",
                "content": f"Say hello to {name}",
            },
        ]

    @mcp.tool()
    async def get_alerts(state: str) -> str:
        """Get weather alerts for a US state (e.g. 'CA', 'NY')."""
        url = f"{NWS_API_BASE}/alerts/active/area/{state}"
        data = await make_nws_request(url)
        if not data or "features" not in data:
            return "Unable to fetch alerts or no alerts found."
        if not data["features"]:
            return "No active alerts for this state."
        alerts = [format_alert(f) for f in data["features"]]
        return "\n\n---\n\n".join(alerts)

    @mcp.tool()
    async def get_forecast(latitude: float, longitude: float) -> str:
        """Get weather forecast for a location."""
        points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
        points_data = await make_nws_request(points_url)
        if not points_data or "properties" not in points_data:
            return "Unable to fetch forecast data for this location."

        forecast_url = points_data["properties"].get("forecast")
        if not forecast_url:
            return "No forecast URL returned by NWS points API."

        forecast_data = await make_nws_request(forecast_url)
        if not forecast_data or "properties" not in forecast_data:
            return "Unable to fetch detailed forecast."

        periods = forecast_data["properties"].get("periods", [])[:5]
        if not periods:
            return "No forecast periods returned."

        chunks = []
        for p in periods:
            chunks.append(
                f"{p.get('name', 'Period')}:\n"
                f"Temperature: {p.get('temperature', '?')}°{p.get('temperatureUnit', '')}\n"
                f"Wind: {p.get('windSpeed', '?')} {p.get('windDirection', '')}\n"
                f"Forecast: {p.get('detailedForecast', '(none)')}"
            )
        return "\n\n---\n\n".join(chunks)

    return server
