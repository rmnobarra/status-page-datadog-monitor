import httpx
from app import config

HEADERS = {
    "DD-API-KEY": config.DATADOG_API_KEY,
    "DD-APPLICATION-KEY": config.DATADOG_APP_KEY,
    "Content-Type": "application/json"
}

async def get_monitor_status(monitor_id: int):
    url = f"{config.DATADOG_API_HOST}/api/v1/monitor/{monitor_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data.get("overall_state")
