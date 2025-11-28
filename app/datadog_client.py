import httpx
from app import config
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "DD-API-KEY": config.DATADOG_API_KEY,
    "DD-APPLICATION-KEY": config.DATADOG_APP_KEY,
    "Content-Type": "application/json"
}

async def get_monitor_status(monitor_id: int):
    """
    Fetch monitor status from Datadog API.
    Returns the overall_state or "No Data" if the monitor doesn't exist or there's an error.
    """
    url = f"{config.DATADOG_API_HOST}/api/v1/monitor/{monitor_id}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            return data.get("overall_state", "No Data")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            logger.warning(f"Monitor {monitor_id} not found in Datadog")
            return "No Data"
        elif e.response.status_code == 403:
            logger.error(f"Access forbidden for monitor {monitor_id}. Check API keys.")
            return "No Data"
        else:
            logger.error(f"HTTP error fetching monitor {monitor_id}: {e}")
            return "No Data"
    except httpx.TimeoutException:
        logger.error(f"Timeout fetching monitor {monitor_id}")
        return "No Data"
    except Exception as e:
        logger.error(f"Unexpected error fetching monitor {monitor_id}: {e}")
        return "No Data"
